from app.api.schemas.house import CreateHouseRequest, UpdateHouseRequest
from app.entities import HouseEntity
from app.exceptions.house_exception import (
    HouseNotFoundByIdError,
    HouseUnathorizadedError,
)
from app.repository.interfaces import HouseRepositoryProtocol
from app.repository.interfaces.house import FilterGetAllHouse


class HouseService:
    def __init__(self, repository: HouseRepositoryProtocol):
        self.repository = repository

    def create_new_house(
        self, user_id: int, request: CreateHouseRequest
    ) -> HouseEntity:
        """
        Crea una nueva casa para el usuario
        Args:
            user_id: id del usuario
            request: data de la casa
        Return:
            HouseEntity: Creada en la db
        """
        new_house = HouseEntity(
            user_id=user_id,
            name=request.name,
            location=request.location,
            invitation_validation=request.invitation_validation,
        )
        house_id = self.repository.create(new_house)
        house = self.repository.get_by_id(house_id)
        if house is None:
            raise Exception
        return house

    def get_all_houses_own_user(self, user_id: int) -> list[HouseEntity]:
        """
        Regresa todas las casa que pertenecen a un usuario
        Args:
            user_id: id del usuario
        Return:
            list[HouseEntity]: Lista de casas pertenecientes a un usuario
        """
        houses = self.repository.get_all(FilterGetAllHouse(user_id=user_id))
        return houses

    def get_house_by_id(self, house_id: int, user_id: int) -> HouseEntity:
        """
        Obtiene una casa mediante su id
        Args:
            house_id identificador único de la casa

        Return:
            HouseEntity

        Notas:
            - Lanza excepción si la casa no se encuentra
        """
        house = self.repository.get_by_id(house_id)
        if house is None:
            raise HouseNotFoundByIdError(house_id)
        # Revisamos que la casa esté autorizada
        if house.user_id != user_id:
            raise HouseUnathorizadedError()

        return house

    def update_house_data(
        self,
        house_id: int,
        request: UpdateHouseRequest,
        user_id: int,
    ) -> bool:
        """
        Actualizamos los datos de la casa
        Args:
            house_id: id de la casa a actualiza
            request: campos a cambiar de la casa

        Return:
            True: Si se actualizó la casa
            False: Si no hay nada que actualizar

        Nota:
            Se lanza excepción si la casa con id no se encuentra
        """

        # Revisa que si exista modificaciones a realizar
        # retorna falso si no hay modificaciones
        if len(request.model_dump(exclude_none=True)) == 0:
            return False

        house = self.repository.get_by_id(house_id)
        if house is None:
            raise HouseNotFoundByIdError(house_id)

        if house.user_id != user_id:
            raise HouseUnathorizadedError()

        if request.location is not None:
            house.location = request.location

        if request.name is not None:
            house.name = request.name

        self.repository.update(house)
        return True

    def delete_house(self, house_id: int, user_id: int) -> None:
        """
        Eliminamos la casa mediante su house_id
        """
        house = self.repository.get_by_id(house_id)
        if house is None:
            raise HouseNotFoundByIdError(user_id)
        if house.user_id != user_id:
            raise HouseUnathorizadedError
        self.repository.delete(house_id)
