from django.shortcuts import render, redirect
from .models import Activity, ActivityLog
from django.contrib.auth.decorators import login_required
from .forms import ActivityForm  # Assumeremo di creare questo form dopo
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import timedelta, datetime
from django.utils import timezone
from .models import Activity, ActivityLog, DayOfWeek
from django.db.models import Count  # Importa Count per il conteggio delle occorrenze
from matplotlib import pyplot as plt
from io import BytesIO  # Importa BytesIO dal modulo io
import base64  # Importa base64
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
from django.utils.safestring import mark_safe



def generate_plot(request):
    """
    Genera un grafico interattivo che mostra la percentuale di completamento delle attività
    dell'utente negli ultimi 60 giorni, utilizzando la media mobile esponenziale per lisciare i dati.
    
    Args:
    request: HttpRequest object.

    Returns:
    Una stringa HTML sicura del grafico generato da Plotly.
    """

    # Fase 1: Calcolo delle date di riferimento
    # Output: current_date, target_date, date_range
    current_date = datetime.now().date()
    target_date = current_date - timedelta(days=60)
    date_range = [target_date + timedelta(days=i) for i in range(61)]

    # Fase 2: Recupero e filtro delle attività dell'utente
    # Output: activities
    activities = Activity.objects.filter(user=request.user)
    traces = []

    # Fase 3: Elaborazione dei dati per ogni attività
    for activity in activities:
        # Fase 3.1: Estrazione e pulizia dei dati dei log
        # Output: distinct_dates
        logs = ActivityLog.objects.filter(activity=activity, date__range=[target_date, current_date])
        distinct_dates = {log.date.date() for log in logs}

        # Fase 3.2: Determinazione dei giorni attivi per l'attività
        # Output: days_active
        if activity.frequency != 'Daily':
            activity_days = DayOfWeek.objects.filter(activity=activity)
            days_of_week_set = {int(day.name) for day in activity_days}
            days_active = [date for date in date_range if date.weekday() in days_of_week_set]
        else:
            days_active = date_range

        # Fase 3.3: Calcolo delle percentuali di completamento
        # Output: percentages
        percentages = [1 if date in distinct_dates else 0 for date in days_active]

        # Fase 3.4: Calcolo dell'EMA basato sui giorni attivi
        # Output: ema
        alpha = 2 / (len(days_active) + 1) if days_active else 0
        ema = [percentages[0]] if percentages else [0]
        for i in range(1, len(percentages)):
            ema.append(alpha * percentages[i] + (1 - alpha) * ema[i - 1])

        # Fase 3.5: Creazione delle tracce del grafico
        # Output: trace
        trace = go.Scatter(
            x=[date.strftime("%Y-%m-%d") for date in days_active],
            y=ema,
            mode='lines+markers',
            name=activity.name
        )
        traces.append(trace)

    # Fase 4: Generazione del grafico finale con Plotly
    # Output: fig, plot_div
    fig = go.Figure(data=traces)
    fig.update_layout(
        title='Percentuale di completamento attività negli ultimi 60 giorni',
        xaxis_title='Data',
        yaxis_title='Percentuale di completamento',
        legend_title='Attività',
        xaxis=dict(tickformat="%Y-%m-%d")
    )
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return mark_safe(plot_div)




@login_required  # Richiede che l'utente sia autenticato per accedere a questa vista
def home(request):
    '''
    Metodo per visualizzare la home page (lista attività con % raggiungimento e menu).
    '''
    # Ottiene tutte le attività associate all'utente loggato
    activities = Activity.objects.filter(user=request.user) #Restituisce una lista di oggetti "Activity" con query user = request.user in cui user è un campo dell'oggetto model di activity
    # Renderizza il template home.html, passando le attività come contesto
    
    #Mi calcolo la % raggiungimento per ogni attivita utente
    completion_percentage = calculate_completion_percentage(request)

    chart_div = generate_plot(request)
    print(chart_div)

    context = {
        'activities': activities,
        'completion_percentage': completion_percentage,
        'chart_image': chart_div,
    }

    return render(request, 'tracker/home.html', context) #Qui prende la richiesta, e invia al template specificato come 2°parametro i dati in una variabile chiamata "activities" e gli passa la variabile locale activities



@login_required
def add_activity(request):
    '''
    Metodo per aggiungere una nuova attività al database.
    '''
    if request.method == 'POST':  # Verifica se il form è stato inviato
        form = ActivityForm(request.POST)  # Crea un form con i dati inviati - ActivityForm è un oggetto creato su forms.py da me.

        if form.is_valid():  # Controlla se il form è valido
            activity = form.save(commit=False)  # Salva l'attività nel database, ma non esegue il commit (attenzione: solo in questo caso se abbiamo relazioni manytomany usare save_m2m dopo il save altrimenti è sufficiente save)
            activity.user = request.user  # Imposta qui l'utente loggato come utente dell'attività
            activity.save()  # Completa il salvataggio dell'attività
            form.save_m2m()  # Salva le relazioni many-to-many - perchè ad un attività vengono assegnati 1 o n giorni.
            return redirect('home')  # Reindirizza l'utente alla home page
    else:
        form = ActivityForm()  # Crea un nuovo form vuoto se non siamo in POST -QUI FACCIO VEDERE IN PRATICA LA PAGINA DI PARTENZA CON FORM VUOTO!
    return render(request, 'tracker/add_activity.html', {'form': form})  # Mostra il form

'''
    form.save(commit=False): Questo è usato per ottenere un'istanza dell'oggetto dal form senza ancora salvare nel database. Ti permette di aggiungere o modificare ulteriori attributi dell'oggetto, come l'utente, prima del salvataggio finale.
    Impostazione dell'Utente: Dopo form.save(commit=False), imposti l'utente come proprietario dell'attività. Questo assicura che tutte le proprietà necessarie siano impostate prima che l'oggetto venga salvato nel database.
    Salvataggio Finale: activity.save() ora salva l'attività nel database con tutti i campi correttamente impostati.
    form.save_m2m(): Questo comando è necessario solo se il tuo form include campi ManyToManyField che non sono stati ancora salvati (dopo un save(commit=False)). Nel tuo caso, potrebbe essere necessario se il campo days_of_week nel form è gestito come ManyToManyField e non hai pre-impostato questi valori in altro modo.
'''


@login_required
def edit_activity(request, pk):
    '''
    Modifica un attività esistente
    '''
    # Ottiene l'attività specificata dall'ID (pk) e che appartiene all'utente loggato
    activity = Activity.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)  # Popola il form con i dati dell'attività
        if form.is_valid():
            form.save()  # Salva le modifiche
            return redirect('home')
    else:
        form = ActivityForm(instance=activity)  # Crea un form prepopolato con i dati esistenti
    return render(request, 'tracker/edit_activity.html', {'form': form})  # Mostra il form


'''
    Se hai configurato correttamente la directory dei template nella tua applicazione Django come `app/templates/app`, allora la chiamata `render` dovrebbe essere corretta come hai indicato:

    ```python
        render(request, 'app/file.html', {'activity': activity})
    ```

    Questo perché stai specificando il percorso relativo al template dalla directory principale dei template della tua applicazione, che è `app/templates/app`. Quindi, quando utilizzi `render`, devi fornire il percorso relativo al tuo template 
    all'interno di questa directory - quindi il percorso della directory "templates".
    Ad esempio, se vuoi renderizzare il file HTML `file.html` all'interno della tua app `app`, il percorso corretto è `'app/file.html'`, come hai indicato. 
    Assicurati che i nomi delle app e dei template siano corretti e che la struttura delle directory sia organizzata in modo appropriato. Se hai problemi con il rendering dei template, potrebbe essere utile verificare anche le impostazioni del 
    tuo server di sviluppo e assicurarti che stia servendo i file statici e dei template correttamente.
'''


@login_required
def delete_activity(request, pk):
    '''
    Elimina un attività
    '''
    # Recupera l'attività specificata dall'ID e verifica che appartenga all'utente loggato
    activity = get_object_or_404(Activity, pk=pk, user=request.user)

    '''
        Il metodo `get_object_or_404()` è una funzione fornita da Django che semplifica il processo di ricerca di un oggetto nel database. Accetta un modello Django e dei p
        arametri di ricerca e tenta di recuperare l'oggetto corrispondente. Se l'oggetto non viene trovato, Django restituisce automaticamente un errore HTTP 404 (Page Not Found), 
        semplificando la gestione degli errori nel tuo codice. Questo metodo è ampiamente utilizzato nelle viste per recuperare oggetti specifici e assicurarsi che siano disponibili 
        prima di procedere con ulteriori operazioni. Utilizzando `get_object_or_404()`, è possibile mantenere il codice più pulito e facile da leggere, migliorando l'esperienza 
        dell'utente e semplificando la manutenzione del codice.
    '''

    if request.method == 'POST':
        # Se il metodo è POST, significa che l'utente ha confermato l'intenzione di eliminare
        activity.delete()
        return redirect('home')  # Reindirizza alla home dopo l'eliminazione
    # Se non è POST, mostra un template di conferma prima di procedere
    return render(request, 'tracker/confirm_delete.html', {'activity': activity}) # Qui nel template avremo la variabile "activity" cui passo l'oggetto activity.




@login_required
def complete_activity(request, pk):
    '''
    Registra il completamento dell'attività nel giorno corrente
    '''
    naive_datetime = datetime.now()  # Questo è un oggetto datetime "naive"
    aware_datetime = make_aware(naive_datetime)  # Converti in un oggetto datetime "aware"

    # Ottieni l'oggetto ActivityLog oppure, se non esiste, crealo.
    log = ActivityLog.objects.create(
        activity_id=pk, 
        date=aware_datetime,  # Assicurati di importare date da datetime
        completed= True
    )

    # Ottieni tutti i log delle attività per l'utente attuale e l'attività specificata
    activity_logs = ActivityLog.objects.filter(activity__user=request.user, activity_id=pk) 
    
    # Ottieni l'ultima data dell'oggetto
    latest_activity_log = ActivityLog.objects.filter(activity=log.activity).latest('date')


    '''
        Nel modello ActivityLog, c'è un campo ForeignKey chiamato activity che fa riferimento al modello Activity. Il campo activity ha a sua volta un campo ForeignKey chiamato user, che fa riferimento al modello User.
        Quindi, quando usi activity__user, stai essenzialmente seguendo il percorso dei ForeignKey per accedere al campo user nel modello Activity associato al log dell'attività. 
        Questo ti consente di filtrare i log delle attività in base all'utente a cui appartiene l'attività associata.
    ''' 

    if request.method == 'POST':
        # Inverti lo stato di completamento dell'attività
        log.completed = True
        log.save()
        return redirect('home')  # Reindirizza alla home dopo l'aggiornamento
    return render(request, 'tracker/complete_activity.html', {'log': log, 'activity_logs' : activity_logs, 'latest_activity_log':latest_activity_log})




@login_required
def delete_activity_log(request, pk):
    '''
    Elimina un log dell' attività specifica.
    '''
    # Recupera la registrazione specificata dall'ID e verifica che l'attività associata appartenga all'utente loggato
    log = get_object_or_404(ActivityLog, pk=pk, activity__user=request.user)
    if request.method == 'POST':
        # Se il metodo è POST, procedi con l'eliminazione
        log.delete()
        return redirect('home')  # Reindirizza alla home dopo l'eliminazione
    # Se non è POST, mostra un template di conferma prima di procedere
    return render(request, 'tracker/confirm_delete_log.html', {'log': log})



@login_required
def delete_old_logs(request,pk):
    '''
    Elimina tutti i log delle attività precedenti a 30 giorni.
    '''
    activity = get_object_or_404(Activity, pk=pk, user=request.user)

    # Calcola la data di 30 giorni fa
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Filtra i log delle attività che sono stati registrati negli ultimi 30 giorni
    logs_to_delete = ActivityLog.objects.filter(date__gte=thirty_days_ago, activity_id=pk)
    
    # Elimina i log selezionati
    logs_to_delete.delete()
    
    return render(request, 'tracker/delete_30_days.html')




@login_required
def calculate_completion_percentage(request):
    """
    Metodo che calcola la percentuale di completamento per ciascuna attività dell'utente.
    Utilizza un range di 7 giorni per determinare il numero totale di giorni previsti
    per le attività e il numero di giorni effettivamente registrati tramite log.
    """
    # Data corrente e data di inizio intervallo di 7 giorni fa
    current_date = datetime.now().date()
    target_date = current_date - timedelta(days=7)

    # Ottieni tutte le attività associate all'utente loggato
    activities = Activity.objects.filter(user=request.user)

    # Lista di tutte le date nell'intervallo di 7 giorni
    days_range = [target_date + timedelta(days=i) for i in range((current_date - target_date).days + 1)]



    # Step1: ----------------------------------------------------------------

    # Dizionario per memorizzare i giorni previsti per ciascuna attività
    total_days = {}

    # Iterazione su ciascuna attività dell'utente
    for activity in activities:
        if activity.frequency == 'Daily':
            days_count = len(days_range)  # Per attività giornaliere, conta tutti i giorni nel range
        else:
            # Ottieni i giorni della settimana associati all'attività e converti il numero del giorno
            activity_days = DayOfWeek.objects.filter(activity=activity)
            days_set = {int(day.name) for day in activity_days}  # Converti il giorno da stringa a intero
            # Calcola i giorni effettivi in cui l'attività era prevista
            days_count = sum(1 for day in days_range if day.weekday() in days_set)

        # Memorizza il numero totale di giorni previsti per l'attività
        total_days[activity.id] = days_count




    # Step2: ----------------------------------------------------------------

    # Dizionario per i giorni effettivamente registrati tramite log
    logged_days = {}

    # Iterazione per calcolare i giorni registrati per ogni attività
    for activity in activities:
        logs = ActivityLog.objects.filter(activity=activity.pk, date__range=(target_date, current_date))
        distinct_dates = {log.date.date() for log in logs}  # Rimuove duplicati mantenendo solo le date
        logged_days_count = len(distinct_dates)  # Conta le date uniche
        logged_days[activity.id] = logged_days_count

    # Calcolo della percentuale di completamento per ciascuna attività
    completion_percentage = {}

    for activity in activities:
        total = total_days.get(activity.id, 0)
        logged = logged_days.get(activity.id, 0)
        if total != 0:
            completion_percentage[activity.id] = (logged / total) * 100
        else:
            completion_percentage[activity.id] = 0

    # Restituisce il dizionario con le percentuali di completamento
    return completion_percentage






'''-------------------------------------colloquio tra vista e template------------------------------------------'''


'''
Nel framework Django, la comunicazione tra le viste (views) e i template è una parte fondamentale del flusso di dati. Le viste gestiscono la logica dell'applicazione, interagendo con il database e processando le informazioni in base alle interazioni degli utenti, mentre i template sono responsabili della presentazione di queste informazioni in un formato leggibile dall'utente.

### Collegamento tra Viste e Template

Quando una vista prepara i dati e chiama un template, passa questi dati attraverso un contesto, che è un dizionario di variabili che il template può utilizzare. Ogni chiave del dizionario nel contesto diventa una variabile accessibile nel template. Vediamo questo processo nel dettaglio, usando la vista `add_activity` come esempio.

#### La Vista `add_activity`

```python
@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)  # Crea un form con i dati inviati
        if form.is_valid():  # Controlla se il form è valido
            activity = form.save(commit=False)  # Salva l'attività nel database, ma non esegue il commit
            activity.user = request.user  # Imposta l'utente corrente come proprietario dell'attività
            activity.save()  # Completa il salvataggio dell'attività
            return redirect('home')  # Reindirizza l'utente alla home page
    else:
        form = ActivityForm()  # Crea un nuovo form vuoto se non siamo in POST

    return render(request, 'tracker/add_activity.html', {'form': form})  # Mostra il form
```

- **`render(request, 'tracker/add_activity.html', {'form': form})`**: Questo è il punto chiave in cui la vista "parla" al template. La funzione `render` è responsabile per compilare il template con i dati. Prende come argomenti l'oggetto `request`, il percorso del template e un dizionario che rappresenta il contesto. In questo caso, il contesto contiene una chiave `'form'` che ha come valore l'oggetto `form` creato nella vista.

#### Il Template `add_activity.html`

```html
{% extends 'base.html' %}

{% block content %}
  <h1>{% if not form.instance.pk %}Aggiungi Attività{% else %}Modifica Attività{% endif %}</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}  <!-- Renderizza ogni campo del form come paragrafo -->
    <button type="submit">Salva</button>
  </form>
{% endblock %}
```

- **`{{ form.as_p }}`**: Questo è dove il template utilizza la variabile `form` passata dalla vista. Il metodo `as_p` è un modo comodo per renderizzare il form dove ogni campo è racchiuso in un tag `<p>`. Questo garantisce che il form sia pronto per l'input dell'utente e che tutti i dati inseriti possano essere gestiti correttamente quando il form viene inviato.

### Flusso di Dati

1. **Utente Invia Richiesta**: L'utente apre la pagina per aggiungere una nuova attività, che invoca la vista `add_activity`.
2. **Vista Elabora Dati**: La vista controlla se è stata ricevuta una richiesta POST (il che indica che il form è stato inviato). Se non è così, prepara un form vuoto.
3. **Vista Passa Dati al Template**: La vista chiama il template `add_activity.html` e gli passa il form attraverso il contesto.
4. **Template Visualizza Dati**: Il template utilizza i dati forniti per costruire la pagina HTML, inclusi i campi del form per l'input dell'utente.

In questo modo, le viste e i template in Django collaborano per gestire e presentare dati dinamicamente in un'applicazione web, mantenendo una chiara separazione tra logica e presentazione.
'''



''' Cosa è il Form Activity usato nelle viste --------------------------------------------------------------------------------------------------------------------'''

'''
La linea `from .forms import ActivityForm` in Django non si riferisce a un oggetto nativo di Django, ma è piuttosto un'importazione di un oggetto definito specificamente per la tua applicazione, nel contesto dell'applicazione stessa. Vediamo in dettaglio cosa significa e come funziona:

### Cos'è `ActivityForm`?

`ActivityForm` è una classe definita all'interno del modulo `forms.py` della tua app Django. Non è un componente standard di Django, ma un componente che crei tu per soddisfare le esigenze specifiche della tua applicazione. Questo modulo di form è tipicamente utilizzato per creare, validare e gestire i dati inviati tramite form HTML.

### Come si Definisce `ActivityForm`?

All'interno del file `forms.py`, utilizzi Django `ModelForm` o `Form` per creare il form. Un `ModelForm` è particolarmente utile quando vuoi che il form sia direttamente collegato a un modello del database, permettendo a Django di gestire automaticamente gran parte della logica di validazione e salvataggio dei dati. Ecco un esempio di come potresti aver definito `ActivityForm`:

```python
from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'frequency', 'days_of_week', 'time_of_day']
        # Puoi anche aggiungere widget personalizzati qui, se necessario
```

In questo esempio:
- **`forms.ModelForm`**: indica che `ActivityForm` è un `ModelForm`, cioè un form di Django che è collegato a un modello specifico.
- **`class Meta`**: una sottoclasse che dice a Django quali informazioni del modello `Activity` includere nel form.
- **`model = Activity`**: specifica che il form è basato sul modello `Activity`.
- **`fields`**: elenca i campi del modello `Activity` che saranno inclusi nel form.

### Perché Importarlo?

L'importazione `from .forms import ActivityForm` nel tuo file `views.py` serve per rendere `ActivityForm` accessibile alle tue viste. In questo modo, quando definisci una vista che necessita di mostrare un form per l'inserimento o la modifica dei dati di un'attività, puoi facilmente istanziare `ActivityForm` e utilizzarlo per gestire i dati del form:

```python
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_view')
    else:
        form = ActivityForm()

    return render(request, 'some_template.html', {'form': form})
```

### Conclusione

`ActivityForm` è quindi un oggetto definito dallo sviluppatore all'interno dell'applicazione Django per gestire specifiche necessità di interazione con i dati dell'utente relative al modello `Activity`. Questo approccio illustra la potenza e la flessibilità di Django nel permettere agli sviluppatori di creare componenti personalizzati che si integrano strettamente con il sistema ORM (Object-Relational Mapping) e il sistema di templating di Django.
'''