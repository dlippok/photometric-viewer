import importlib.metadata
from dataclasses import dataclass

@dataclass
class ProjectUrls:
    homepage: str
    bug_tracker: str
    support: str

@dataclass
class ProjectMetadata:
    id: str
    name: str
    version: str
    developer_name: str
    urls: ProjectUrls
    copyright: str


def _get_metadata():
    metadata = importlib.metadata.metadata('photometric-viewer')
    project_urls = {
        i.split(", ")[0]: i.split(", ")[1]
        for i
        in metadata.get_all('Project-URL') or {}
    }

    return ProjectMetadata(
        id='io.github.dlippok.photometric-viewer',
        name='Photometry',
        version=metadata['version'],
        developer_name=metadata["Author"],
        urls=ProjectUrls(
            homepage=metadata["Home-page"],
            bug_tracker=project_urls.get("Issues", None),
            support=project_urls.get("Support", None),
        ),
        copyright="© 2023 Damian Lippok"
    )


PROJECT = _get_metadata()
