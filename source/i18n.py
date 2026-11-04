"""Small, complete message catalog for the five SysLinuxOS UI languages."""

import os


CATALOGS = {
    "en": {
        "title": "Network Neighbors", "subtitle": "Devices connected to this computer's network ports",
        "refresh": "Refresh", "interface": "Local interface", "device": "Neighbor", "port": "Remote port",
        "protocol": "Protocol", "vlan_pvid": "Port VLAN (PVID)", "details": "Details", "port_description": "Port description",
        "chassis_id": "Chassis ID", "management_ip": "Management IP", "none": "—",
        "scanning": "Reading neighbors…", "empty": "No neighbors reported yet. Check the cable and LLDP on the switch, then refresh.",
        "found": "{count} neighbor(s) found", "not_installed": "lldpd is not installed.",
        "daemon_unavailable": "Cannot read lldpd. Check that its service is running and that you have access to its socket.",
        "timeout": "The LLDP service did not respond in time.", "invalid_data": "The LLDP service returned data this app cannot read.",
        "authorization_failed": "Authorization was cancelled or failed.",
        "read_only": "This app only reads neighbors. LLDP transmission is controlled by the lldpd service.",
    },
    "it": {
        "title": "Vicini di rete", "subtitle": "Dispositivi collegati alle porte di rete di questo computer",
        "refresh": "Aggiorna", "interface": "Interfaccia locale", "device": "Vicino", "port": "Porta remota",
        "protocol": "Protocollo", "vlan_pvid": "VLAN porta (PVID)", "details": "Dettagli", "port_description": "Descrizione porta",
        "chassis_id": "ID chassis", "management_ip": "IP di gestione", "none": "—",
        "scanning": "Lettura dei vicini…", "empty": "Nessun vicino segnalato. Controlla il cavo e LLDP sullo switch, poi aggiorna.",
        "found": "Vicini trovati: {count}", "not_installed": "lldpd non è installato.",
        "daemon_unavailable": "Impossibile leggere lldpd. Controlla che il servizio sia attivo e l'accesso al suo socket.",
        "timeout": "Il servizio LLDP non ha risposto in tempo.", "invalid_data": "Il servizio LLDP ha restituito dati non leggibili dall'app.",
        "authorization_failed": "Autorizzazione annullata o non riuscita.",
        "read_only": "L'app legge soltanto i vicini. La trasmissione LLDP dipende dal servizio lldpd.",
    },
    "fr": {
        "title": "Voisins réseau", "subtitle": "Appareils connectés aux ports réseau de cet ordinateur",
        "refresh": "Actualiser", "interface": "Interface locale", "device": "Voisin", "port": "Port distant",
        "protocol": "Protocole", "vlan_pvid": "VLAN du port (PVID)", "details": "Détails", "port_description": "Description du port",
        "chassis_id": "ID du châssis", "management_ip": "IP de gestion", "none": "—",
        "scanning": "Lecture des voisins…", "empty": "Aucun voisin signalé. Vérifiez le câble et LLDP sur le commutateur, puis actualisez.",
        "found": "Voisins trouvés : {count}", "not_installed": "lldpd n'est pas installé.",
        "daemon_unavailable": "Lecture de lldpd impossible. Vérifiez le service et l'accès à son socket.",
        "timeout": "Le service LLDP n'a pas répondu à temps.", "invalid_data": "Le service LLDP a renvoyé des données illisibles.",
        "authorization_failed": "Autorisation annulée ou échouée.",
        "read_only": "L'application lit seulement les voisins. Le service lldpd contrôle les annonces LLDP.",
    },
    "de": {
        "title": "Netzwerknachbarn", "subtitle": "Geräte an den Netzwerkanschlüssen dieses Computers",
        "refresh": "Aktualisieren", "interface": "Lokale Schnittstelle", "device": "Nachbar", "port": "Entfernter Port",
        "protocol": "Protokoll", "vlan_pvid": "Port-VLAN (PVID)", "details": "Details", "port_description": "Portbeschreibung",
        "chassis_id": "Chassis-ID", "management_ip": "Management-IP", "none": "—",
        "scanning": "Nachbarn werden gelesen…", "empty": "Keine Nachbarn gemeldet. Kabel und LLDP am Switch prüfen und aktualisieren.",
        "found": "Gefundene Nachbarn: {count}", "not_installed": "lldpd ist nicht installiert.",
        "daemon_unavailable": "lldpd kann nicht gelesen werden. Dienst und Socket-Zugriff prüfen.",
        "timeout": "Der LLDP-Dienst hat nicht rechtzeitig geantwortet.", "invalid_data": "Der LLDP-Dienst hat unlesbare Daten geliefert.",
        "authorization_failed": "Autorisierung abgebrochen oder fehlgeschlagen.",
        "read_only": "Diese App liest nur Nachbarn. Der Dienst lldpd steuert LLDP-Ankündigungen.",
    },
    "es": {
        "title": "Vecinos de red", "subtitle": "Dispositivos conectados a los puertos de red de este equipo",
        "refresh": "Actualizar", "interface": "Interfaz local", "device": "Vecino", "port": "Puerto remoto",
        "protocol": "Protocolo", "vlan_pvid": "VLAN del puerto (PVID)", "details": "Detalles", "port_description": "Descripción del puerto",
        "chassis_id": "ID del chasis", "management_ip": "IP de gestión", "none": "—",
        "scanning": "Leyendo vecinos…", "empty": "No se detectan vecinos. Compruebe el cable y LLDP en el switch y actualice.",
        "found": "Vecinos encontrados: {count}", "not_installed": "lldpd no está instalado.",
        "daemon_unavailable": "No se puede leer lldpd. Compruebe el servicio y el acceso a su socket.",
        "timeout": "El servicio LLDP no respondió a tiempo.", "invalid_data": "El servicio LLDP devolvió datos ilegibles.",
        "authorization_failed": "Autorización cancelada o fallida.",
        "read_only": "La aplicación solo lee vecinos. El servicio lldpd controla los anuncios LLDP.",
    },
}


def choose_language(environ=None):
    environ = os.environ if environ is None else environ
    locale = next((environ[key] for key in ("LC_ALL", "LC_MESSAGES", "LANG") if environ.get(key)), "en")
    if locale.split(".")[0] in ("C", "POSIX"):
        return "en"
    for candidate in (environ.get("LANGUAGE", "").split(":") if environ.get("LANGUAGE") else []) + [locale]:
        language = candidate.split("_")[0].split(".")[0].lower()
        if language in CATALOGS:
            return language
    return "en"


def tr(language, key, **values):
    return CATALOGS[language][key].format(**values)
