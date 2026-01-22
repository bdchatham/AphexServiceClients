from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChunkResult")


@_attrs_define
class ChunkResult:
    """
    Attributes:
        content (Union[Unset, str]): Chunk text content
        source (Union[Unset, str]): Source document path
        chunk_index (Union[Unset, int]): Index within source document
        score (Union[Unset, float]): Similarity score
    """

    content: Union[Unset, str] = UNSET
    source: Union[Unset, str] = UNSET
    chunk_index: Union[Unset, int] = UNSET
    score: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        source = self.source

        chunk_index = self.chunk_index

        score = self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if source is not UNSET:
            field_dict["source"] = source
        if chunk_index is not UNSET:
            field_dict["chunk_index"] = chunk_index
        if score is not UNSET:
            field_dict["score"] = score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content", UNSET)

        source = d.pop("source", UNSET)

        chunk_index = d.pop("chunk_index", UNSET)

        score = d.pop("score", UNSET)

        chunk_result = cls(
            content=content,
            source=source,
            chunk_index=chunk_index,
            score=score,
        )

        chunk_result.additional_properties = d
        return chunk_result

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
