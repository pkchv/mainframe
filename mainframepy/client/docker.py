import os
from typing import Literal, Optional

import docker
from docker.models.containers import Container

app_data_directory = os.path.realpath("~/.app-data")


def create_container(
    image_id: str,
    image_version: str = "latest",
    volumes: Optional[list[(Literal["config", "models", "outputs"], str)]] = None,
) -> Container:
    dckr = docker.from_env()

    container = dckr.containers.run(
        f"{image_id}:{image_version}",
        ports={"8080": None},
        detach=True,
        device_requests=[
            docker.types.DeviceRequest(device_ids=["0"], capabilities=[["gpu"]])
        ],
        volumes=_create_volume_binds(app_data_directory, image_id, volumes),
    )

    container.reload()

    return container


def _create_volume_binds(
    app_data_directory: str,
    image_id: str,
    volumes: Optional[list[(Literal["config", "models", "outputs"], str)]] = None,
):
    _volumes = {
        os.path.join(app_data_directory, image_id, "config"): {
            "bind": "/config",
            "mode": "ro",
        },
        os.path.join(app_data_directory, image_id, "models"): {
            "bind": "/models",
            "mode": "rw",
        },
        os.path.join(app_data_directory, image_id, "outputs"): {
            "bind": "/outputs",
            "mode": "rw",
        },
    }

    if volumes is not None:
        for volume in volumes:
            _volumes[os.path.join(app_data_directory, image_id, volume[0])] = {
                "bind": volume[1],
                "mode": "rw",
            }

    return _volumes


def get_host_port(container: Container) -> int:
    return int(container.attrs["NetworkSettings"]["Ports"]["8080/tcp"][0]["HostPort"])


def exit(container: Container):
    container.stop()
    container.remove()
