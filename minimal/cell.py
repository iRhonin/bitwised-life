from nanohttp import settings
from restfulpy.orm import Field, DeclarativeBase, DBSession
from sqlalchemy import Integer, BOOLEAN
from sqlalchemy import UniqueConstraint
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import column_property
from sqlalchemy.orm import object_session


class CellPopError(Exception):
    pass


class Cell(DeclarativeBase):
    __tablename__ ='cell'

    CITY_RADIUS = 1

    id = Field(Integer, primary_key=True)

    is_alive = Field(BOOLEAN, default=False)
    is_deleted = Field(BOOLEAN, default=False)

    x = Field(Integer)
    y = Field(Integer)

    city_population = column_property(
        select([func.sum(is_alive)])
            .where(x.between(x - CITY_RADIUS, x + CITY_RADIUS))
            .where(y.between(y - CITY_RADIUS, y + CITY_RADIUS))
    )

    UniqueConstraint(x, y, name='ux_x_y')

    @property
    def session(self):
        return object_session(self)

    def die(self):
        self.is_alive = False
        self.is_deleted = True

    def revive(self):
        self.is_alive = True
        self.is_deleted = False

    def clone(self):
        clone = type(self)(
            is_alive=self.is_alive,
            x=self.x,
            y=self.y,
        )
        self.session.add(clone)

    def update(self):
        if self.is_alive:
            if settings.city.min_population <= self.city_population <= settings.city.max_population:
                pass
            elif self.city_population < settings.city.min_population:
                self.die()
            elif self.city_population > settings.city.max_population:
                self.die()
            return

        # cell is dead
        if self.city_population == settings.city.birth_population:
            self.revive()

        return

    @classmethod
    def pop(cls, session=DBSession):
        find_query = session.query(cls.id, cls.is_deleted) \
            .filter(cls.is_deleted == False) \
            .limit(1) \
            .with_for_update()

        cte = find_query.cte('find_query')
        cell = session.query(cls).join(cte, cte.c.id == cls.id).one_or_none()
        if cell is None:
            raise CellPopError()

        return cell

    def execute(self, session=DBSession):
        try:
            isolated_cell = session \
                .query(Cell) \
                .filter(Cell.id == self.id) \
                .one()
            isolated_cell.update()
            session.commit()
        except:
            session.rollback()
            raise
