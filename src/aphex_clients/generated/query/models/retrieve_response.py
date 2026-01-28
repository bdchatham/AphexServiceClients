from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chunk_result import ChunkResult


T = TypeVar("T", bound="RetrieveResponse")


@_attrs_define
class RetrieveResponse:
    """
    Attributes:
        chunks (Union[Unset, list['ChunkResult']]):
        query (Union[Unset, str]):
    """

    chunks: Union[Unset, list["ChunkResult"]] = UNSET
    query: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chunks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.chunks, Unset):
            chunks = []
            for chunks_item_data in self.chunks:
                chunks_item = chunks_item_data.to_dict()
                chunks.append(chunks_item)

        query = self.query

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if chunks is not UNSET:
            field_dict["chunks"] = chunks
        if query is not UNSET:
            field_dict["query"] = query

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.chunk_result import ChunkResult

        d = src_dict.copy()
        chunks = []
        _chunks = d.pop("chunks", UNSET)
        for chunks_item_data in _chunks or []:
            chunks_item = ChunkResult.from_dict(chunks_item_data)

            chunks.append(chunks_item)

        query = d.pop("query", UNSET)

        retrieve_response = cls(
            chunks=chunks,
            query=query,
        )

        retrieve_response.additional_properties = d
        return retrieve_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
