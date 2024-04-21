from django.db import models
from django.contrib.auth.models import User


# Definizione del modello per i giorni della settimana.
class DayOfWeek(models.Model):
    name = models.CharField(max_length=10)  # Nome abbreviato del giorno (es. "Mon" per lunedì)
    display_name = models.CharField(max_length=50)  # Nome completo del giorno (es. "Monday" per lunedì)

    def __str__(self):
        return self.display_name  # Restituisce il nome completo del giorno quando viene chiamato il metodo str()


# Definizione del modello per le attività dell'utente.
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    # Collegamento con l'utente che ha creato l'attività
    name = models.CharField(max_length=100)  # Nome dell'attività
    description = models.TextField()  # Descrizione dell'attività
    
    # Frequenza dell'attività, con scelte predefinite come giornaliera, settimanale o mensile
    frequency = models.CharField(max_length=50, choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')])
    
    #Associazione vs entità dayofweek
    days_of_week = models.ManyToManyField(DayOfWeek)  # Giorni della settimana in cui si svolge l'attività
    
    # Opzioni per l'orario del giorno, da 06:00 a 23:00
    TIME_OF_DAY_CHOICES = [(f"{i:02d}:00", f"{i:02d}:00") for i in range(6, 24)]
    time_of_day = models.CharField(max_length=5, choices=TIME_OF_DAY_CHOICES)  # Orario del giorno dell'attività

    def __str__(self):
        return self.name  # Restituisce il nome dell'attività quando viene chiamato il metodo str()


# Definizione del modello per i log delle attività.
class ActivityLog(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="logs")
    # Collegamento con l'attività a cui si riferisce questo log
    date = models.DateTimeField()  # Aggiornato a DateTimeField per includere l'orario
  
    completed = models.BooleanField(default=False)  # Indica se l'attività è stata completata o meno

    def __str__(self):
        return f"{self.activity.name} log for {self.date} completed: {self.completed}"
        # Restituisce una stringa descrittiva del log quando viene chiamato il metodo str()



'''
    In Django, quando definisci un modello, non è necessario specificare esplicitamente un campo per la chiave primaria (PK, Primary Key) se non hai esigenze particolari. Django gestisce automaticamente la creazione di un campo id come 
    chiave primaria intera autoincrementante per ogni modello che crei, a meno che tu non specifichi diversamente.

inoltre nelle relazioni:

        - **ForeignKey**: Utilizzata quando un oggetto può appartenere a uno e un solo altro oggetto.
        - Esempio: Un libro appartiene a un unico autore.

        - **ManyToManyField**: Utilizzata quando un oggetto può essere associato a più istanze di un altro oggetto e viceversa.
        - Esempio: Un libro può appartenere a più categorie e una categoria può contenere più libri.

    In sostanza, la differenza principale sta nel tipo di relazione che desideri modellare nel tuo database: uno-a-molti (ForeignKey) o molti-a-molti (ManyToManyField).

'''
