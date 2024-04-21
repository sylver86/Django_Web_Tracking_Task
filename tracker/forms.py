from django import forms
from .models import Activity  # Importa il modello Activity dal modulo models.

# Quindi abbiamo associato al modello Activity il suo Form.

class ActivityForm(forms.ModelForm):
    """
    Form per la creazione o modifica delle attività basato sul modello Activity.
    Questo form utilizza Django forms.ModelForm che facilita la creazione di form
    direttamente da modelli Django, automatizzando processi come la validazione dei dati.
    """

    class Meta:
        model = Activity  # Specifica quale modello usare per costruire questo form.
        fields = ['name', 'description', 'frequency', 'days_of_week', 'time_of_day']
        # 'fields' definisce quali campi del modello devono essere esposti nel form.

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # Widget Textarea per il campo description, con attributi HTML per controllarne le dimensioni.

            'frequency': forms.Select(attrs={'class': 'form-control'}),
            # Widget Select per il campo frequency, che renderizza una selezione dropdown
            # basata sulle scelte definite nel modello.

            'days_of_week': forms.CheckboxSelectMultiple(),
            # Widget Select per il campo days_of_week, che permette la selezione singola
            # da un elenco di opzioni.

            'time_of_day': forms.Select(),
            # Widget Select per il campo time_of_day, che renderizza un menu a tendina
            # per selezionare un orario specifico.
        }

        labels = {
            'name': 'Nome Attività',
            'description': 'Descrizione',
            'frequency': 'Frequenza',
            'days_of_week': 'Giorno della Settimana',
            'time_of_day': 'Orario del Giorno'
        }
        # 'labels' permette di specificare le etichette personalizzate per i campi nel form,
        # sostituendo i nomi dei campi con stringhe più user-friendly.



'''

### Cosa sono i Widgets in Django Forms?

    I **widgets** in Django Forms sono componenti che definiscono come i campi del form vengono renderizzati in HTML e come i dati di input vengono gestiti. Essi controllano l'aspetto visivo del campo di input in una pagina web, 
    oltre a definire come l'input dell'utente viene raccolto e trasformato in dati che Django può usare e validare. I widget possono essere personalizzati con attributi HTML specifici, come classi CSS, stili, placeholder e altro per 
    migliorare l'usabilità e l'integrazione con il frontend.

    Per esempio, nel tuo `ActivityForm`, il widget `Textarea` per il campo `description` è configurato con dimensioni specifiche (`cols=40` e `rows=5`), che influenzano direttamente come il campo è visualizzato nel browser. 
    Questo permette di adattare l'interfaccia utente alle tue necessità specifiche.

### Cosa Fa la Classe Meta in un ModelForm?

    La classe `Meta` dentro un `ModelForm` in Django è un posto dove vengono definite le configurazioni specifiche di quel form. La presenza di questa classe interna serve a comunicare a Django varie opzioni su come il form deve essere gestito. V
    ediamo i componenti principali:

        - **model**: Indica a Django quale modello è usato per costruire questo form. Questo collegamento tra il modello e il form permette a Django di automatizzare molte operazioni, come la generazione di campi del form basati sui campi del modello, 
        e la validazione e la pulizia dei dati in base ai tipi di dati e alle restrizioni definite nel modello.

        - **fields**: Specifica quali campi del modello dovrebbero essere inclusi nel form. Puoi includere tutti i campi, escluderli esplicitamente o definire esplicitamente solo quelli che vuoi includere. Questo ti dà controllo su quali parti del 
        modello sono esposte per l'editing tramite il form.

        - **widgets**: Associa specifici widget ai campi del form, come mostrato nel tuo esempio. Questo controllo dettagliato sui widget permette di migliorare significativamente l'interazione dell'utente con il form.

        - **labels**: Permette di specificare etichette personalizzate per i campi nel form, che possono essere utilizzate per sovrascrivere i nomi predefiniti dei campi o per rendere l'interfaccia più user-friendly.

### Esempi dalla Tua Configurazione

    Nel tuo form, la classe `Meta` definisce specificamente:

    - **Modello utilizzato**: `Activity`.
    - **Campi inclusi**: `name`, `description`, `frequency`, `days_of_week`, `time_of_day`.
    - **Widgets personalizzati**: per esempio, il `CheckboxSelectMultiple` per `days_of_week`, che permette selezioni multiple in forma di checkbox, un'interfaccia utente molto più accessibile per la selezione di più opzioni rispetto a un semplice dropdown.

    Questa configurazione assicura che il form sia non solo funzionale ma anche integrato con l'esperienza utente desiderata, rendendo i form di Django estremamente potenti e flessibili per sviluppatori web.

'''