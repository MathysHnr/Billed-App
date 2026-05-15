# Plan de test End-to-End du parcours administrateur RH

Ce document décrit le plan de test End-to-End (E2E) du parcours administrateur
RH de l'application Billed. Chaque scénario est exprimé au format Given / When
/ Then.

## I. Authentification (page Login)

### Scénario 1
| | |
|---|---|
| **Given** | Je suis un visiteur (non connecté). |
| **When** | Je ne remplis pas le champ e-mail ou le champ password du login administrateur et je clique sur le bouton « Se connecter ». |
| **Then** | Je reste sur la page Login et je suis invité à remplir le champ manquant. |

### Scénario 2
| | |
|---|---|
| **Given** | Je suis un visiteur (non connecté). |
| **When** | Je remplis le champ e-mail du login administrateur au mauvais format (sans la forme chaîne@chaîne) et je clique sur le bouton « Se connecter ». |
| **Then** | Je reste sur la page Login et je suis invité à remplir le champ e-mail au bon format. |

### Scénario 3
| | |
|---|---|
| **Given** | Je suis un visiteur (non connecté). |
| **When** | Je remplis le champ e-mail et le champ password du login administrateur dans le bon format et je clique sur le bouton « Se connecter ». |
| **Then** | Je suis authentifié en tant qu'administrateur RH et je suis redirigé vers la page Dashboard (« Validations »). |

### Scénario 4
| | |
|---|---|
| **Given** | Je suis un administrateur authentifié sur la page Dashboard. |
| **When** | Je rafraîchis la page ou je reviens sur l'application. |
| **Then** | Ma session est conservée (via le localStorage) et je reste sur la page Dashboard sans devoir me reconnecter. |

## II. Page Dashboard – vue globale des notes de frais

### Scénario 5
| | |
|---|---|
| **Given** | Je suis un administrateur RH authentifié. |
| **When** | J'arrive sur la page Dashboard. |
| **Then** | Je vois trois sections (« En attente », « Validé », « Refusé ») avec le nombre de notes de frais pour chaque statut, ainsi que la zone « Validations » à droite avec la grande icône Billed. |

### Scénario 6
| | |
|---|---|
| **Given** | Je suis sur la page Dashboard et au moins une note de frais existe pour le statut « En attente ». |
| **When** | Je clique sur la flèche de la section « En attente ». |
| **Then** | La section se déplie et affiche la liste des cartes des notes de frais correspondantes (nom de l'employé, libellé, montant, date, type). |

### Scénario 7
| | |
|---|---|
| **Given** | Je suis sur la page Dashboard et la section « En attente » est dépliée. |
| **When** | Je clique à nouveau sur la flèche de la même section. |
| **Then** | La section se replie et les cartes des notes de frais associées ne sont plus affichées. |

### Scénario 8
| | |
|---|---|
| **Given** | Je suis sur la page Dashboard et plusieurs sections sont dépliées simultanément. |
| **When** | Je clique sur la flèche d'une autre section (par exemple « Validé »). |
| **Then** | La section ciblée se déplie indépendamment des autres ; chaque section conserve son propre état (ouvert/fermé). |

## III. Page Dashboard – consultation d'une note de frais

### Scénario 9
| | |
|---|---|
| **Given** | Je suis sur la page Dashboard et la section « En attente » est dépliée. |
| **When** | Je clique sur la carte d'une note de frais. |
| **Then** | Le formulaire de détail de la note de frais s'affiche à droite (type, nom, date, commentaire, montant, TVA, justificatif) et les boutons « Refuser » et « Accepter » apparaissent car la note est au statut « En attente ». |

### Scénario 10
| | |
|---|---|
| **Given** | Je suis sur la page Dashboard et le formulaire de détail d'une note de frais est ouvert. |
| **When** | Je clique une deuxième fois sur la carte de la même note de frais. |
| **Then** | Le formulaire de détail se ferme et la grande icône Billed (`big-billed-icon`) réapparaît à droite. |

### Scénario 11
| | |
|---|---|
| **Given** | Je suis sur la page Dashboard et le formulaire de détail d'une note de frais est ouvert. |
| **When** | Je clique sur l'icône en forme d'œil située dans le formulaire. |
| **Then** | Une modale s'ouvre et affiche le justificatif (image du reçu) associé à la note de frais. |

## IV. Page Dashboard – validation / refus d'une note de frais

### Scénario 12
| | |
|---|---|
| **Given** | Je suis sur la page Dashboard et le formulaire d'une note de frais au statut « En attente » est ouvert. |
| **When** | Je saisis éventuellement un commentaire puis je clique sur le bouton « Accepter ». |
| **Then** | Le statut de la note de frais passe à « accepted », mon commentaire est enregistré et je suis redirigé vers la vue principale du Dashboard. |

### Scénario 13
| | |
|---|---|
| **Given** | Je suis sur la page Dashboard et le formulaire d'une note de frais au statut « En attente » est ouvert. |
| **When** | Je saisis éventuellement un commentaire puis je clique sur le bouton « Refuser ». |
| **Then** | Le statut de la note de frais passe à « refused », mon commentaire est enregistré et je suis redirigé vers la vue principale du Dashboard. |

## V. Déconnexion

### Scénario 14
| | |
|---|---|
| **Given** | Je suis un administrateur RH authentifié sur n'importe quelle page de l'application. |
| **When** | Je clique sur l'icône de déconnexion dans la barre verticale gauche. |
| **Then** | Ma session est supprimée du localStorage et je suis redirigé vers la page Login. |
