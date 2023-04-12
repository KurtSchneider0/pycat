import typing
import category

T = typing.TypeVar("T")

class ObjectFunction(typing.Generic[T]):

    def __init__(self, domain: set[category.Object[T]], codomain: set[category.Object[T]]) -> None:
        self.domain = domain
        self.codomain = codomain


class ArrowFunction(typing.Generic[T]):

    def __init__(self, domain: set[category.Morphism[T]], codomain: set[category.Morphism[T]]) -> None:
        self.domain = domain
        self.codomain = codomain


class Functor(typing.Generic[T]):
    
    def __init__(self, domain: category.Category[T], codomain: category.Category[T], objectfunction: ObjectFunction[T], arrowfunction: ArrowFunction[T]) -> None:
        self.domain = domain
        self.codomain = codomain
        self.objectfunction = objectfunction
        self.arrowfunction = arrowfunction

    def compose(self, functor):
        return CompositeFunctor(functor, self)
    

class IdentityFunctor(Functor):

    def __init__(self, codomain: category.Category[T]) -> None:
        self.codomain = codomain


class NamedFunctor(Functor):

    def __init__(self, domain: category.Category[T], codomain: category.Category[T], name: str) -> None:
        self.domain = domain
        self.codomain = codomain
        self.name = name

class CompositeFunctor(Functor):

    def __init__(self, functor1: Functor[T], functor2: Functor[T]) -> None:
        self.functor1 = functor1
        self.functor2 = functor2

    @property 
    def objectcomponents(self) -> tuple:
        if isinstance(self.functor1, CompositeFunctor):
            if isinstance(self.functor2, CompositeFunctor):
                return (*self.functor2.objectcomponents, *self.functor1.objectcomponents)
            else:
                return (self.functor2, *self.functor1.objectcomponents)
        elif isinstance(self.functor2, IdentityFunctor):
            return self.functor1
        else:
            return (self.functor2, self.functor1)

    @property 
    def arrowcomponents(self) -> tuple:
        if isinstance(self.functor1, CompositeFunctor):
            if isinstance(self.functor2, CompositeFunctor):
                return (*self.functor2.arrowcomponents, *self.functor1.arrowcomponents)
            else:
                return (self.functor2, *self.functor1.arrowcomponents)
        elif isinstance(self.functor2, IdentityFunctor):
            return self.functor1
        else:
            return (self.functor2, self.functor1)

    @property 
    def domain(self) -> category.Category[T]:
        return self.functor1.domain
    
    @property 
    def codomain(self) -> category.Category[T]:
        return self.functor2.codomain