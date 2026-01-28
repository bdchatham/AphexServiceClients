from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReadyResponse")


@_attrs_define
class ReadyResponse:
    """
    Attributes:
        status (Union[Unset, str]):
        embedding_service (Union[Unset, str]):
        vector_store (Union[Unset, str]):
    """

    status: Union[Unset, str] = UNSET
    embedding_service: Union[Unset, str] = UNSET
    vector_store: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        embedding_service = self.embedding_service

        vector_store = self.vector_store

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if embedding_service is not UNSET:
            field_dict["embedding_service"] = embedding_service
        if vector_store is not UNSET:
            field_dict["vector_store"] = vector_store

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status", UNSET)

        embedding_service = d.pop("embedding_service", UNSET)

        vector_store = d.pop("vector_store", UNSET)

        ready_response = cls(
            status=status,
            embedding_service=embedding_service,
            vector_store=vector_store,
        )

        ready_response.additional_properties = d
        return ready_response

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
