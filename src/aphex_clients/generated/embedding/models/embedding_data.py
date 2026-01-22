from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbeddingData")


@_attrs_define
class EmbeddingData:
    """
    Attributes:
        object_ (Union[Unset, str]):  Default: 'embedding'.
        embedding (Union[Unset, list[float]]):
        index (Union[Unset, int]):
    """

    object_: Union[Unset, str] = "embedding"
    embedding: Union[Unset, list[float]] = UNSET
    index: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_

        embedding: Union[Unset, list[float]] = UNSET
        if not isinstance(self.embedding, Unset):
            embedding = self.embedding

        index = self.index

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_ is not UNSET:
            field_dict["object"] = object_
        if embedding is not UNSET:
            field_dict["embedding"] = embedding
        if index is not UNSET:
            field_dict["index"] = index

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        object_ = d.pop("object", UNSET)

        embedding = cast(list[float], d.pop("embedding", UNSET))

        index = d.pop("index", UNSET)

        embedding_data = cls(
            object_=object_,
            embedding=embedding,
            index=index,
        )

        embedding_data.additional_properties = d
        return embedding_data

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
