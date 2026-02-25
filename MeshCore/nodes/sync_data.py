import argparse
import enum
import json
import requests
import objectrest
import os
import time
from abc import abstractmethod, ABC
from pydantic import BaseModel
from typing import Optional
from urllib.parse import quote

MESHMAPPER_REPEATERS_URL = "https://den.meshmapper.net/repeaters.json"  # Only repeaters in Denver
LETSMESH_NODES_URL = "https://api.letsmesh.net/api/nodes?region=DEN"  # All devices in Denver


### Generic models

class NodeType(enum.Enum):
    """
    Enum representing the type of given node, used throughout the logic here
    """
    REPEATER = 1
    ROOM_SERVER = 2
    COMPANION = 3

    @classmethod
    def from_int(cls, role: int) -> 'NodeType':
        if role == 1:
            return cls.REPEATER
        elif role == 2:
            return cls.ROOM_SERVER
        elif role == 3:
            return cls.COMPANION
        else:
            raise ValueError(f"Unknown device role: {role}")


class BaseNode(BaseModel, ABC):
    """
    An abstract base class representing a node, either from an API or used internally.
    """
    pass

    @abstractmethod
    def public_key_id(self) -> str:
        """
        Return the first byte (2-character hex string) of the public key, which is used as an identifier for the node.
        :return: The first byte of the public key as a hex string.
        :rtype: str
        """
        raise NotImplementedError("Subclasses must implement the public_key_id property")


class Node(BaseNode):
    """
    Internal representation of a generic node.
    Used for processing and comparing nodes from multiple API sources.
    """
    public_key: str
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    node_type: NodeType
    is_observer: bool = False
    contact: str | None
    created_at: int  # Unix timestamp
    last_heard: int  # Unix timestamp

    @property
    def public_key_id(self) -> str:
        """
        Return the first two bytes (4-character hex string) of the public key, which is used as an identifier for the node.
        Always returns the public key ID in uppercase to ensure consistency when comparing with other nodes.
        :return: The first two bytes of the public key as a hex string, in uppercase.
        :rtype: str
        """
        return self.public_key_id_4_char

    @property
    def public_key_id_4_char(self) -> str:
        """
        Return the first two bytes (4-character hex string) of the public key, which is used as an identifier for the node.
        Always returns the public key ID in uppercase to ensure consistency when comparing with other nodes.
        :return: The first two bytes of the public key as a hex string, in uppercase.
        :rtype: str
        """
        return self.public_key[:4].upper()

    @property
    def public_key_id_2_char(self) -> str:
        """
        Return the first byte (2-character hex string) of the public key, which is used as an identifier for the node.
        Always returns the public key ID in uppercase to ensure consistency when comparing with other nodes.
        :return: The first byte of the public key as a hex string, in uppercase.
        :rtype: str
        """
        return self.public_key[:2].upper()

    @property
    def hash(self) -> int:
        """
        Generate a hash value for this node
        :return: An integer hash value representing this node.
        """
        _input = f"{self.name}:{self.public_key_id}:{self.node_type.value}:{self.latitude}:{self.longitude}:{self.is_observer}"
        return hash(_input)

    def to_json(self) -> dict:
        """
        Serialize this node to a JSON-compatible dictionary
        :return: A dictionary representation of this node that can be serialized to JSON.
        """
        return {
            'public_key': self.public_key,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'node_type': self.node_type.value,
            'is_observer': self.is_observer,
            'contact': self.contact,
            'created_at': self.created_at,
            'last_heard': self.last_heard,
        }


### MeshMapper-specific models for parsing API responses

class MeshMapperRepeater(BaseModel):
    id: str
    hex_id: str
    name: str
    lat: float
    lon: float
    last_heard: int  # Unix timestamp
    created_at: str  # Unix timestamp as string
    enabled: int
    power: str
    iata: str


### LetsMesh-specific models for parsing API responses

class LetsMeshNodeRole(enum.Enum):
    """
    Enum representing the device role of a node in the LetsMesh network, as returned by the LetsMesh API.
    """
    COMPANION = 1
    REPEATER = 2
    ROOM = 3

    @classmethod
    def from_int(cls, role: int) -> 'LetsMeshNodeRole':
        if role == 1:
            return cls.COMPANION
        elif role == 2:
            return cls.REPEATER
        elif role == 3:
            return cls.ROOM
        else:
            raise ValueError(f"Unknown device role: {role}")

    @property
    def to_node_type(self) -> NodeType:
        if self == LetsMeshNodeRole.COMPANION:
            return NodeType.COMPANION
        elif self == LetsMeshNodeRole.REPEATER:
            return NodeType.REPEATER
        elif self == LetsMeshNodeRole.ROOM:
            return NodeType.ROOM_SERVER
        else:
            raise ValueError(f"Unknown device role: {self.value}")


class LetsMeshNodeLocation(BaseModel):
    """
    Represents the location of a node as returned by the LetsMesh API.
    """
    latitude: float
    longitude: float


class LetsMeshNode(BaseModel):
    """
    Represents a node as returned by the LetsMesh API.
    """
    public_key: str
    name: str
    device_role: LetsMeshNodeRole
    regions: list[str]
    first_seen: str  # ISO 8601 timestamp
    last_seen: str  # ISO 8601 timestamp
    is_mqtt_connected: bool
    location: Optional[LetsMeshNodeLocation] = None


def _get_letsmesh_nodes() -> list[LetsMeshNode]:
    """
    Fetch nodes from the LetsMesh API for the Denver region and return them as a list of LetsMeshNode objects.
    :return: A list of LetsMeshNode objects representing the nodes in the Denver region.
    :rtype: list[LetsMeshNode]
    """
    res = requests.get(url=LETSMESH_NODES_URL,
                       headers={
                           "Host": "api.letsmesh.net",
                           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:147.0) Gecko/20100101 Firefox/147.0",
                           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                           "Accept-Language": "en-US,en;q=0.9",
                           "Accept-Encoding": "gzip, deflate, br, zstd",
                           "Connection": "keep-alive",
                       }, timeout=10)
    print(res)
    print(res.text)

    return objectrest.get_object(url=LETSMESH_NODES_URL,  # type: ignore
                                 model=LetsMeshNode,
                                 extract_list=True,
                                 sub_keys=["nodes"],
                                 headers={
                                     "Host": "api.letsmesh.net",
                                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:147.0) Gecko/20100101 Firefox/147.0",
                                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                     "Accept-Language": "en-US,en;q=0.9",
                                     "Accept-Encoding": "gzip, deflate, br, zstd",
                                     "Connection": "keep-alive",
                                 })


def _get_meshmapper_repeaters() -> list[MeshMapperRepeater]:
    """
    Fetch repeaters from the MeshMapper API for the Denver region and return them as a list of MeshMapperRepeater objects.
    :return: A list of MeshMapperRepeater objects representing the repeaters in the Denver region.
    :rtype: list[MeshMapperRepeater]
    """
    return objectrest.get_object(url=MESHMAPPER_REPEATERS_URL,  # type: ignore
                                 model=MeshMapperRepeater,
                                 extract_list=True)


def _get_city_name(lat, lon):
    if lat is None or lon is None:
        return None

    try:
        headers = {'User-Agent': 'MeshCore-DEN-Sync/1.0'}
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18"
        data = objectrest.get_json(url=url, headers=headers, timeout=10)
        address = data.get('address', {})
        return (
                address.get('neighbourhood')  # Most specific
                or address.get('suburb')
                or address.get('village')
                or address.get('town')
                or address.get('city')
                or address.get('municipality')
        )
    except Exception as e:
        print(f"Error geocoding {lat}, {lon}: {e}")
        return None


def _meshmapper_node_is_room(node: MeshMapperRepeater, letsmesh_nodes: list[LetsMeshNode]) -> bool:
    # MeshMapper doesn't specify node types,
    # but if there's a LetsMesh node with the same public key and it's a room server,
    # we can infer that this MeshMapper node is also a room server
    for lm_node in letsmesh_nodes:
        if lm_node.public_key.upper() == node.hex_id.upper():
            return lm_node.device_role == LetsMeshNodeRole.ROOM

    return False


def _build_contact_url(name: str, public_key: str) -> str:
    encoded_name = quote(name)
    return f"meshcore://contact/add?name={encoded_name}&public_key={public_key.upper()}&type=2"


def _iso8601_to_unix_timestamp(iso_str: str) -> int:
    if not iso_str:
        return 0

    try:
        # e.g. 2026-02-18T01:19:00.379Z
        dt = time.strptime(iso_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return int(time.mktime(dt))
    except Exception as e:
        return 0


def get_den_repeaters() -> list[Node]:
    """
    Get all nodes in the Denver region (repeaters, room servers, and companions)
    :return: A list of Node objects representing all nodes in the Denver region.
    :rtype: list[Node]
    """
    meshmapper_repeaters: list[MeshMapperRepeater] = _get_meshmapper_repeaters()
    letsmesh_nodes: list[LetsMeshNode] = _get_letsmesh_nodes()

    return [
        Node(
            public_key=repeater.hex_id,
            name=repeater.name,
            latitude=repeater.lat,
            longitude=repeater.lon,
            # This may take time, that's why this doesn't run often
            node_type=(NodeType.ROOM_SERVER
                       if (_meshmapper_node_is_room(node=repeater, letsmesh_nodes=letsmesh_nodes) and letsmesh_nodes)
                       else NodeType.REPEATER),
            is_observer=False,  # Unknown
            contact=_build_contact_url(name=repeater.name, public_key=repeater.hex_id),
            created_at=int(repeater.created_at) if repeater.created_at.isdigit() else 0,
            last_heard=repeater.last_heard,
        )
        for repeater in meshmapper_repeaters
    ]


def get_den_companions() -> list[Node]:
    """
    Get all companion nodes in the Denver region.
    :return: A list of Node objects representing all companion nodes in the Denver region.
    :rtype: list[Node]
    """
    letsmesh_nodes: list[LetsMeshNode] = _get_letsmesh_nodes()
    return [
        Node(
            public_key=node.public_key,
            name=node.name,
            latitude=node.location.latitude if node.location else None,
            longitude=node.location.longitude if node.location else None,
            node_type=node.device_role.to_node_type,
            is_observer=not node.is_mqtt_connected,
            contact=_build_contact_url(name=node.name, public_key=node.public_key),
            created_at=_iso8601_to_unix_timestamp(node.first_seen),
            last_heard=_iso8601_to_unix_timestamp(node.last_seen),
        )
        for node in letsmesh_nodes
        # Only include companions
        if node.device_role == LetsMeshNodeRole.COMPANION
    ]


def is_reserved_public_key_id(public_key_id: str) -> bool:
    """
    Check if a public key ID is reserved.
    :param public_key_id: The public key ID to check (2 or 4 hex characters).
    :type public_key_id: str
    :return: True if the public key ID is reserved, False otherwise.
    :rtype: bool
    """
    if public_key_id[:2].upper() in ["00", "FF"]:  # Reserved by LetsMesh/MeshMapper
        return True

    # ref: https://ottawamesh.ca/deployment/repeaters-intercity/
    if public_key_id[:1].upper() in ['A']:  # A-block reserved by DenverMesh for future use
        return True

    return False


def are_same_node(node_1: Node, node_2: Node) -> bool:
    """
    Determine if two nodes represent the same node.
    :param node_1: The first node to compare.
    :param node_2: The second node to compare.
    :return: True if the nodes are the same, False otherwise.
    """
    if node_1.public_key.upper() == node_2.public_key.upper():
        return True

    return False


def _read_nodes_from_file(file_path: str) -> list[Node]:
    nodes = []
    if not os.path.exists(file_path):
        return nodes

    with open(file_path, "r", encoding="utf-8") as f:
        _data = json.load(f)
        for item in _data:
            nodes.append(
                Node(**item)
            )
    return nodes


def _filter_diff_nodes(existing_nodes: list[Node], new_nodes: list[Node]) -> tuple[list[Node], list[Node], list[Node]]:
    """
    Filter nodes into three categories:
    1) New nodes that are in new_nodes but not in existing_nodes
    2) Duplicate nodes that are in both existing_nodes and new_nodes
    3) Missing nodes that are in existing_nodes and not in new_nodes (potentially removed nodes)
    :param existing_nodes: The list of existing nodes to compare against.
    :param new_nodes: The list of new nodes to compare with existing nodes.
    :return: A tuple containing three lists: (new_nodes_list, duplicate_nodes_list, missing_nodes_list)
    """
    all_nodes = {}

    existing_node_hash_map = {}
    new_node_hash_map = {}

    # Loop through the "existing" nodes to build a map of hashes of their identifiers
    # and store all nodes in a combined map for easy lookup
    for node in existing_nodes:
        _hash = node.hash
        existing_node_hash_map[_hash] = _hash
        all_nodes[_hash] = node

    # Loop through the "new" nodes to build a map of hashes of their identifiers
    # and store all nodes in a combined map for easy lookup
    for node in new_nodes:
        _hash = node.hash
        new_node_hash_map[_hash] = _hash
        all_nodes[_hash] = node

    # Prepare sets
    existing_nodes_set = set(existing_node_hash_map.items())
    new_nodes_set = set(new_node_hash_map.items())

    true_new_nodes = new_nodes_set - existing_nodes_set
    duplicate_nodes = new_nodes_set & existing_nodes_set
    missing_nodes = existing_nodes_set - new_nodes_set

    # Look up the actual Node objects for each category based on the hashes and return them as lists
    return (
        list(all_nodes[_hash] for _hash, _ in true_new_nodes),
        list(all_nodes[_hash] for _hash, _ in duplicate_nodes),
        list(all_nodes[_hash] for _hash, _ in missing_nodes),
    )


def sync_repeaters(storage_file_path: str) -> None:
    print(f"Fetching repeaters from {MESHMAPPER_REPEATERS_URL}...")
    repeaters: list[Node] = get_den_repeaters()
    print(f"Found {len(repeaters)} repeaters from MeshMapper API")

    existing_repeaters: list[Node] = _read_nodes_from_file(file_path=storage_file_path)
    print(f"Loaded {len(existing_repeaters)} known repeaters from cache")

    new, duplicate, missing = _filter_diff_nodes(existing_nodes=existing_repeaters, new_nodes=repeaters)
    print(
        f"Found {len(new)} new repeaters, {len(duplicate)} duplicate repeaters, and {len(missing)} missing repeaters compared to cache")

    if new or missing:
        # Write ALL repeaters to file
        print("Updating cache with new repeaters...")
        with open(storage_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([node.to_json() for node in repeaters], ensure_ascii=False, indent=2))
        print("Cache updated.")
    else:
        print("No changes detected, cache not updated.")


def sync_companions(storage_file_path: str) -> None:
    print(f"Fetching companions from {LETSMESH_NODES_URL}...")
    companions: list[Node] = get_den_companions()
    print(f"Found {len(companions)} companions from LetsMesh API")

    existing_companions: list[Node] = _read_nodes_from_file(file_path=storage_file_path)
    print(f"Loaded {len(existing_companions)} known companions from cache")

    new, duplicate, missing = _filter_diff_nodes(existing_nodes=existing_companions, new_nodes=companions)
    print(
        f"Found {len(new)} new companions, {len(duplicate)} duplicate companions, and {len(missing)} missing companions compared to cache")

    if new or missing:
        # Write ALL repeaters to file
        print("Updating cache with new repeaters...")
        with open(storage_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([node.to_json() for node in companions], ensure_ascii=False, indent=2))
        print("Cache updated.")
    else:
        print("No changes detected, cache not updated.")


def main(repeater_data_file: str, companion_data_file: str) -> None:
    print("Starting LetsMesh sync...")

    print("Syncing repeaters...")
    sync_repeaters(storage_file_path=repeater_data_file)

    print("Syncing companions...")
    sync_companions(storage_file_path=companion_data_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for changes to MeshCore devices in Denver.")
    parser.add_argument(
        "--repeaters-data-file",
        type=str,
        help="Path to the data file to store repeater information.",
        required=True
    )
    parser.add_argument(
        "--companions-data-file",
        type=str,
        help="Path to the data file to store companion information.",
        required=True
    )
    args = parser.parse_args()

    repeater_data_file = args.repeaters_data_file
    companion_data_file = args.companions_data_file
    main(repeater_data_file=repeater_data_file, companion_data_file=companion_data_file)
