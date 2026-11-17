from datetime import date, datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, model_validator


class ReservationBase(BaseModel):
    date_debut: date
    date_fin: date
    nb_personnes: int = Field(gt=0)
    id_chambre: int = Field(gt=0)

    @model_validator(mode="after")
    def verifier_dates(self):
        aujourd_hui = datetime.now(
            ZoneInfo("Europe/Paris")
        ).date()

        if self.date_debut < aujourd_hui:
            raise ValueError(
                "Une réservation ne peut pas commencer dans le passé"
            )

        if self.date_fin <= self.date_debut:
            raise ValueError(
                "Le départ doit être après l'arrivée"
            )

        return self


class ReservationCreate(ReservationBase):
    id_client: int = Field(gt=0)
