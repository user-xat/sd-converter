import numpy as np
import recognizers.text_recognizer as text_recognizer
from typing import Union
from pydantic import BaseModel, Field
from model.object_types import ObjectType
import model.elements as elems


class SDWrappedElement(BaseModel):
    this: Union[elems.SDElement, None]
    coef: float = Field(default=0.75)
    parent: Union["SDWrappedElement", None] = Field(default=None, init=False)
    sub_elements: list["SDWrappedElement"] = Field(default_factory=list, init=False)

    def find_sub_elements(self) -> None:
        elem_for_remove: list = list()
        for elem1  in self.sub_elements:
            if elem1 in elem_for_remove:
                continue

            for elem2 in self.sub_elements:
                if elem1 == elem2 or elem2 in elem_for_remove:
                    continue

                coef1 = elem1.this.contain_elem(elem2.this)
                coef2 = elem2.this.contain_elem(elem1.this)
                final_coef = coef1 if coef1 > coef2 else coef2
                if final_coef > self.coef:
                    elem1.sub_elements.append(elem2)
                    elem_for_remove.append(elem2)
                    #elem2.parent = elem1

        # delete sub elements
        self.sub_elements = [x for x in self.sub_elements if x not in elem_for_remove]
        [x.find_sub_elements() for x in self.sub_elements] # find sub-sub elements

    def items(self):
        if self.this:
            yield self.this
        for elem in self.sub_elements:
            yield from elem.items()

    def get_attributes(self, orig_img: np.ndarray, objects: list[elems.SDObject]) -> None:
        if self.this and self.this.has_text():
            text = self._get_text(orig_img, self.this.xyxy)
            if isinstance(self.this, elems.SDNote):
                self.this.body = text
            else:
                self.this.name = text

        elem_for_remove: list = list()
        for elem  in self.sub_elements:
            if elem.this.cls == ObjectType.label:
                text = self._get_text(orig_img, elem.this.xyxy)

                elem_for_remove.append(elem)
                if isinstance(self.this, elems.SDPackage):
                    self.this.name = text
            elif elem.this.cls == ObjectType.terminator:
                for obj in objects:
                    if obj.contain_section_x(elem.this):
                        obj.terminator = True
                        obj.xyxy = (obj.xyxy[0], obj.xyxy[1], obj.xyxy[2], elem.this.xyxy[3])
                        break
                elem_for_remove.append(elem)

        self.sub_elements = [x for x in self.sub_elements if x not in elem_for_remove]
        [x.get_attributes(orig_img, objects) for x in self.sub_elements]

    def _get_text(self, orig_img, xyxy):
        sub_img = text_recognizer.sub_image(orig_img, xyxy)
        text = text_recognizer.recognize_text(sub_img).strip()
        text = text.replace('\n\n', '\n')
        return text 