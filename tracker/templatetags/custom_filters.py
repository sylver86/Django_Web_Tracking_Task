from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, "0%")  # Default to "0%" if key is not found


'''
In Django, i filtri sono utili strumenti del sistema di template che permettono di modificare le variabili prima che vengano visualizzate nel template. Possono essere visti come funzioni che vengono applicate ai valori delle variabili per trasformarli, formattarli o manipolarli in qualche modo prima di renderli nell'HTML. I filtri sono usati principalmente per due scopi: formattazione e trasformazione dei dati.

### Esempi di Filtri Comuni in Django:
1. **`date`**: Formatta un oggetto datetime secondo un formato specifico. Per esempio:
   ```django
   {{ my_date_variable|date:"D d M Y" }}
   ```
   Questo trasformerà la data in un formato leggibile come "Wed 09 Apr 2021".

2. **`length`**: Restituisce la lunghezza di una stringa o di una lista.
   ```django
   {{ my_list|length }}
   ```

3. **`lower`**: Converte una stringa in minuscolo.
   ```django
   {{ "HELLO"|lower }}
   ```

4. **`upper`**: Converte una stringa in maiuscolo.
   ```django
   {{ "hello"|upper }}
   ```

5. **`default`**: Fornisce un valore di default se il valore originale è considerato falso (come `None`, `False`, una stringa vuota, ecc.).
   ```django
   {{ my_variable|default:"No data" }}
   ```

6. **`truncatechars`**: Tronca una stringa a un numero specifico di caratteri e aggiunge un suffisso, solitamente "...".
   ```django
   {{ my_long_string|truncatechars:10 }}
   ```

### Come Creare un Filtro Personalizzato:
Se i filtri integrati non soddisfano le tue esigenze, Django ti permette di definire filtri personalizzati. Ecco i passaggi per crearne uno:

1. **Crea la directory `templatetags`** all'interno della tua app Django se non esiste già.
2. **Aggiungi un file Python** (ad esempio, `custom_filters.py`) e includi il codice per definire e registrare il tuo filtro.
3. **Definisci il filtro** usando un decoratore `@register.filter`:
   ```python
   from django import template

   register = template.Library()

   @register.filter
   def my_custom_filter(value, arg):
       # Manipola il valore e restituisci il risultato
       return do_something_with(value, arg)
   ```

4. **Carica e usa il filtro nel template**:
   ```django
   {% load custom_filters %}
   {{ my_variable|my_custom_filter:"some_argument" }}
   ```

I filtri personalizzati possono essere molto potenti per manipolare dati nel contesto del template, permettendo di mantenere il codice Python separato dalla logica di presentazione e mantenendo i template puliti e leggibili.
'''