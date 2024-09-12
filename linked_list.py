from typing import Any, Iterable, NoReturn


class MetaLinkedListIterator(type):
    def __new__(cls, name, bases, attrs):
        attrs['__slots__'] = ('_node')
        return super().__new__(cls, name, bases, attrs)


class Node:
    __slots__ = (
        "data",
        "next_node"
    )

    def __init__(self, _data: Any = None):
        self.data = _data
        self.next_node = None


class LinkedListIterator(metaclass=MetaLinkedListIterator):
    def __init__(self, _link_list):
        self._node: Node = _link_list.head

    def __iter__(self):
        return self

    def __next__(self) -> Node:
        if self._node is None:
            raise StopIteration

        _node: Node = self._node
        self._node = _node.next_node
        return _node


class ValueLinkedListIterator(LinkedListIterator):
    def __next__(self) -> Any:
        _node = super().__next__()
        return _node.data


class LinkedList:
    __slots__ = (
        "head",
        "last_node",
        "length"
    )

    def __init__(self, _iter: Iterable | None = None):
        self.head = None
        self.last_node = None
        self.length = 0

        if _iter is None:
            return

        for _el in _iter:
            self.add(_el)

    def add(self, _data: Any) -> None:
        _node = Node(_data)
        self.length += 1

        if self.head is None:
            self.head = self.last_node = _node
            return

        self.last_node.next_node = _node
        self.last_node = _node
    
    def insert(self, _data, *, index):
        if index < 0:
            raise IndexError("Index out of range")

        new_node = Node(_data)

        if index == 0:
            new_node.next_node = self.head
            self.head = new_node
            return

        if index == self.length:
            self.add(_data)
            return

        current = self.head
        for _ in range(index - 1):
            if current is None:
                raise IndexError("Index out of range")
            current = current.next_node

        if current is None:
            raise IndexError("Index out of range")

        new_node.next_node = current.next_node
        current.next_node = new_node
        self.length += 1

    def __repr__(self) -> str:
        repr_str = ""

        for el in self:
            repr_str += f"{repr(el)} -> "

        return f"[ {repr_str[:-4]} ]"

    def __iter__(self) -> ValueLinkedListIterator:
        return ValueLinkedListIterator(self)

    def nodes(self) -> LinkedListIterator:
        return LinkedListIterator(self)

    def __next__(self) -> NoReturn:
        raise TypeError(f"'{self.__class__.__name__}' object is not an iterator")

    def remove(self, _data: Any) -> None:
        _head = self.head
        _no_data = ValueError(f"Value {repr(_data)} not in linked list")

        if _head is None:
            raise _no_data

        if _data == _head.data:
            self.head = _head.next_node
            self.length -= 1
            return

        for node in self.nodes():
            _next_node = node.next_node

            if _next_node is not None and _data == _next_node.data:
                node.next_node = _next_node.next_node
                self.length -= 1
                break
        else:
            raise _no_data
    
    def pop(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        
        if index == 0:
            _pop_data = self.head.data
            self.head = self.head.next_node
            self.length -= 1
            return _pop_data

        for i, node in enumerate(self.nodes()):
            _next_node = node.next_node

            if _next_node is not None and i == index - 1:
                _pop_data = _next_node.data
                node.next_node = _next_node.next_node
                self.length -= 1
                return _pop_data


if __name__ == '__main__':
    l = LinkedList(i for i in range(10))
    print(l)

    l.pop(4)
    print(l)
