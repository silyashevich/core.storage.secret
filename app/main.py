import asyncio
import json
import logging
import os
import signal
import sys
import uuid

import redis.asyncio as redis
from aiohttp import web
from jsonschema import exceptions, validate

sys.tracebacklimit = 0

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)

handler.setFormatter(formatter)
logger.addHandler(handler)

PORT = os.environ.get("PORT", "2081")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost")
logger.info("app internal port: %r", PORT)
logger.info("redis url: %r", REDIS_URL)


secret_post_schema = {
    "type": "object",
    "properties": {
        "expiration": {"type": "number"},
        "message": {"type": "string"},
        "one_time": {"type": "boolean"},
    },
    "required": [
        "expiration",
        "message",
    ],
    "additionalProperties": False,
    "minProperties": 2,
}

router = web.RouteTableDef()

HOSTNAME: str = os.environ.get("HOSTNAME", "Unknown")

_ns = {
    "http_requests_secret_post": 0,
    "http_requests_secret_post_ok": 0,
    "http_requests_secret_post_err": 0,
    "http_requests_secret_get": 0,
    "http_requests_secret_get_ok": 0,
    "http_requests_secret_get_miss": 0,
    "http_requests_secret_get_err": 0,
}


class AioHttpAppException(BaseException):
    """An exception specific to the AioHttp application."""


class ResetException(AioHttpAppException):
    """Exception raised when an application reset is requested."""


class GracefulExitException(AioHttpAppException):
    """Exception raised when an application exit is requested."""


def handle_sighup() -> None:
    logging.warning("Received SIGHUP")
    raise ResetException("Application reset requested via SIGHUP")


def handle_sigterm() -> None:
    logging.warning("Received SIGTERM")
    raise ResetException("Application exit requested via SIGTERM")


def cancel_tasks() -> None:
    for task in asyncio.all_tasks():
        task.cancel()


@router.get("/health")
async def health(request: web.Request) -> web.Response:
    return web.Response(text="HEALTHY")


@router.get("/metrics")
async def metrics(request: web.Request) -> web.Response:
    data = ""
    for _ in _ns:
        data += '%s{server="%s"} %s\n' % (_, HOSTNAME, _ns[_])
    return web.Response(text=data)


@router.post("/secret")
async def secret_post(request: web.Request) -> web.Response:
    _ns["http_requests_secret_post"] += 1
    try:
        instance = json.loads(await request.text())
        try:
            validate(
                instance=instance,
                schema=secret_post_schema,
            )
        except exceptions.ValidationError as err:
            logger.exception("json data is not valid, exception: %r", err)
            _ns["http_requests_secret_post_err"] += 1
            return web.json_response(data=err, status=400)
        key = str(uuid.uuid4())
        r = await redis.from_url(REDIS_URL)
        async with r.pipeline(transaction=True) as pipe:
            await pipe.set(key, json.dumps(instance)).expire(
                key, instance.get("expiration")
            ).execute()
        logger.info("secret %s was created", key)
        _ns["http_requests_secret_post_ok"] += 1
        return web.json_response(  # оригинал кидает просто текст
            {
                "message": key,
            }
        )
    except json.JSONDecodeError as err:
        logger.exception("json data is bad, exception: %r", err)
        return web.json_response(data=err.msg, status=400)


@router.get(
    r"/secret/{key:[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}}"
)
async def secret_get(request: web.Request) -> web.Response:
    _ns["http_requests_secret_get"] += 1
    key = request.match_info["key"]
    r = await redis.from_url(REDIS_URL)
    async with r.pipeline(transaction=True) as pipe:
        exists, data = await pipe.exists(key).get(key).execute()
    if exists:
        try:
            instance = json.loads(data)
        except json.JSONDecodeError as err:
            _ns["http_requests_secret_get_err"] += 1
            logger.exception("secret %s has bad data, exception: %r", key, err)
            return web.json_response(data=err.msg, status=400)
        if instance.get("one_time"):
            async with r.pipeline(transaction=True) as pipe:
                await pipe.delete(key).execute()
            logger.info("secret %s was deleted", key)
    else:
        logger.error("secret %s does not exist", key)
        _ns["http_requests_secret_get_miss"] += 1
        return web.json_response(data={"message": "Secret not found"}, status=404)
    logger.info("secret %s was received", key)
    _ns["http_requests_secret_get_ok"] += 1
    return web.json_response(data=instance, status=200)


def run_app() -> bool:
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGHUP, handle_sighup)
    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)
    app = web.Application()
    app.add_routes(router)
    try:
        web.run_app(app, port=int(PORT), handle_signals=True)
    except ResetException:
        logging.warning("Reloading...")
        cancel_tasks()
        asyncio.set_event_loop(asyncio.new_event_loop())
        return True
    except GracefulExitException:
        logging.warning("Exiting...")
        cancel_tasks()
        loop.close()
    return False


def main() -> None:
    while run_app():
        pass


if __name__ == "__main__":
    main()
