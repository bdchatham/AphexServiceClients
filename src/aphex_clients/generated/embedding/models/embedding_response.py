from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.embedding_data import EmbeddingData
    from ..models.embedding_usage import EmbeddingUsage


T = TypeVar("T", bound="EmbeddingResponse")


@_attrs_define
class EmbeddingResponse:
    """
    Attributes:
        object_ (Union[Unset, str]):  Default: 'list'.
        data (Union[Unset, list['EmbeddingData']]):
        model (Union[Unset, str]):
        usage (Union[Unset, EmbeddingUsage]):
    """

    object_: Union[Unset, str] = "list"
    data: Union[Unset, list["EmbeddingData"]] = UNSET
    model: Union[Unset, str] = UNSET
    usage: Union[Unset, "EmbeddingUsage"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_

        data: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        model = self.model

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_ is not UNSET:
            field_dict["object"] = object_
        if data is not UNSET:
            field_dict["data"] = data
        if model is not UNSET:
            field_dict["model"] = model
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.embedding_data import EmbeddingData
        from ..models.embedding_usage import EmbeddingUsage

        d = src_dict.copy()
        object_ = d.pop("object", UNSET)

        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = EmbeddingData.from_dict(data_item_data)

            data.append(data_item)

        model = d.pop("model", UNSET)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, EmbeddingUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = EmbeddingUsage.from_dict(_usage)

        embedding_response = cls(
            object_=object_,
            data=data,
            model=model,
            usage=usage,
        )

        embedding_response.additional_properties = d
        return embedding_response

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
