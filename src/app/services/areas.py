from app.api.schemas.area import CreateAreaRequest, UpdateAreaRequest
from app.entities import AreaEntity
from app.exceptions.areas_exceptions import (
    AreaNotFoundByIdError,
    DuplicateNameAreaError,
)
from app.repository.interfaces import AreaRepositoryProtocol, FilterAreas


class AreaService:
    def __init__(self, repository: AreaRepositoryProtocol):
        self.repository = repository

    def get_areas_by_house_id(self, house_id: int) -> list[AreaEntity]:
        """Obtiene todas las áreas asociadas a una casa específica.

        Args:
            house_id (int): El ID de la casa para la cual se obtendrán las áreas.

        Returns:
            list[AreaEntity]: Una lista de entidades de área pertenecientes a la casa.
        """
        filters = FilterAreas(house_id=house_id)
        return self.repository.get_all(filters)

    def get_area_by_id(self, area_id: int) -> AreaEntity:
        """Obtiene una área específica por su ID.

        Args:
            area_id (int): El ID único del área a obtener.

        Returns:
            AreaEntity: La entidad del área encontrada.

        Raises:
            AreaNotFoundByIdError: Si no se encuentra el área con el ID proporcionado.
        """
        area = self.repository.get_by_id(area_id)
        if area is None:
            raise AreaNotFoundByIdError(area_id)
        return area

    def create_area(self, house_id: int, area_data: CreateAreaRequest) -> int:
        """Crea una nueva área en una casa específica.

        Args:
            house_id (int): El ID de la casa donde se creará el área.
            area_data (CreateAreaRequest): Un objeto con los datos del área
            (name, type).

        Returns:
            int: El ID de la nueva área creada.

        Raises:
            DuplicateNameAreaError: Si ya existe un área con el mismo nombre en la casa.
            DatabaseConstraintException: Si hay una violación de restricciones.
        """
        # Verificar duplicado
        existing_areas = self.repository.get_all(FilterAreas(house_id=house_id))
        if any(a.name.lower() == area_data.name.lower() for a in existing_areas):
            raise DuplicateNameAreaError(area_data.name, house_id)

        area = AreaEntity(
            house_id=house_id,
            name=area_data.name,
            type=area_data.type,
        )
        return self.repository.create(area)

    def patch_area(self, area_id: int, request: UpdateAreaRequest) -> bool:
        """Actualiza parcialmente una área existente.

        Args:
            area_id (int): El ID del área a actualizar.
            area_data (UpdateAreaRequest): Un objeto con los campos a actualizar
            (name, type).

        Raises:
            AreaNotFoundByIdError: Si no se encuentra el área con el ID proporcionado.
            DuplicateNameAreaError: Si ya existe otra área con el mismo nombre en la
            casa.
            DatabaseConstraintException: Si hay una violación de restricciones durante
            la actualización.
        """
        if len(request.model_dump(exclude_none=True)) == 0:
            return False

        area = self.repository.get_by_id(area_id)
        if area is None:
            raise AreaNotFoundByIdError(area_id)

        # Verificar duplicado si se cambia el nombre
        if request.name is not None:
            existing_areas = self.repository.get_all(
                FilterAreas(house_id=area.house_id)
            )
            if any(
                a.name.lower() == request.name.lower() and a.id != area_id
                for a in existing_areas
            ):
                raise DuplicateNameAreaError(request.name, area.house_id)
            area.name = request.name

        if request.type is not None:
            area.type = request.type
        self.repository.update(area)
        return True

    def delete_area(self, area_id: int) -> None:
        """Elimina una área por su ID.

        Args:
            area_id (int): El ID del área a eliminar.

        Raises:
            AreaNotFoundByIdError: Si no se encuentra el área con el ID proporcionado.
        """
        area = self.repository.get_by_id(area_id)
        if area is None:
            raise AreaNotFoundByIdError(area_id)
        self.repository.delete(area_id)
