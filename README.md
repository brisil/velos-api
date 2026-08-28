# velos-api

API HTTP légère (Flask) qui expose l'état d'un système de vélos en libre-service :
stations disponibles, quartiers, taux d'occupation, alertes de pénurie.

## Routes

- `/sante` : état de santé de l'application
- `/stations` : liste des stations avec quartier et vélos disponibles
- `/disponibilite` : taux d'occupation moyen du parc
- `/alertes` : stations dont le nombre de vélos disponibles est inférieur ou égal à deux
