# Plan de test End-to-End du parcours administrateur RH

Ce document décrit le plan de test End-to-End (E2E) du parcours administrateur
RH de l'application Billed. Chaque scénario est exprimé au format Given / When
/ Then.

## Scénario 1
| | |
|---|---|
| **Given** | Je suis un visiteur (non connecté). |
| **When** | Je ne remplis pas le champ e-mail ou le champ password du login administrateur et je clique sur le bouton "Se connecter". |
| **Then** | Je reste sur la page Login et je suis invité à remplir le champ manquant. |

## Scénario 2
| | |
|---|---|
| **Given** | Je suis un visiteur (non connecté). |
| **When** | Je remplis le champ e-mail du login administrateur au mauvais format (sans la forme chaîne@chaîne) et je clique sur le bouton "Se connecter". |
| **Then** | Je reste sur la page Login et je suis invité à remplir le champ e-mail au bon format. |

## Scénario 3
| | |
|---|---|
| **Given** | Je suis un visiteur (non connecté). |
| **When** | Je remplis le champ e-mail du login administrateur au bon format (sous la forme chaîne@chaîne), le champ password du login administrateur et je clique sur le bouton "Se connecter". |
| **Then** | Je suis envoyé sur la page Dashboard. |

## Scénario 4
| | |
|---|---|
| **Given** | Je suis connecté en tant qu'administrateur. |
| **When** | Je clique sur un ticket de note de frais et il est en statut "en attente". |
| **Then** | Le formulaire de la note de frais est affiché avec l'ensemble des champs remplis sauf son statut. Il est modifiable. |

## Scénario 5
| | |
|---|---|
| **Given** | Je suis connecté en tant qu'administrateur et j'ai cliqué sur un ticket "en attente". |
| **When** | Je clique sur le champ "commentaire". |
| **Then** | Je peux insérer un commentaire. |

## Scénario 6
| | |
|---|---|
| **Given** | Je suis connecté en tant qu'administrateur et j'ai cliqué sur un ticket "en attente". |
| **When** | Je clique sur le bouton "accepter". |
| **Then** | Le statut de la note de frais apparaît comme "accepté" dans le feed des notes de frais. Le nombre de notes de frais du groupe "accepté" est incrémenté de 1 et le statut apparaît comme "accepté" dans le tableau de notes de frais de l'employé qui l'avait envoyée. |

## Scénario 7
| | |
|---|---|
| **Given** | Je suis connecté en tant qu'administrateur et j'ai cliqué sur un ticket "en attente". |
| **When** | Je clique sur le bouton "refuser". |
| **Then** | Le statut de la note de frais apparaît comme "refusé" dans le feed des notes de frais. Le nombre de notes de frais du groupe "refusé" est incrémenté de 1 et le statut apparaît comme "refusé" dans le tableau de notes de frais de l'employé qui l'avait envoyée. |

## Scénario 8
| | |
|---|---|
| **Given** | Je suis connecté en tant qu'administrateur. |
| **When** | Je clique sur un ticket de note de frais et il est en statut "accepté" ou "refusé". |
| **Then** | Le formulaire de la note de frais ticket est affiché avec l'ensemble des champs remplis y compris son statut. Il n'est plus modifiable. |

## Scénario 9
| | |
|---|---|
| **Given** | Je suis connecté en tant qu'administrateur et j'ai cliqué sur une note de frais en statut "en attente", ou "accepté" ou "refusé". |
| **When** | Je clique sur le bouton Visualiser. |
| **Then** | Une modale apparaît avec le PDF du justificatif. |

## Scénario 10
| | |
|---|---|
| **Given** | Je suis connecté en tant qu'administrateur et j'ai cliqué sur une note de frais en statut "en attente", ou "accepté" ou "refusé". |
| **When** | Je clique sur le bouton "Télécharger". |
| **Then** | Le PDF du justificatif est téléchargé. |

## Scénario 11
| | |
|---|---|
| **Given** | Je suis connecté en tant qu'administrateur et je suis sur la page Dashboard. |
| **When** | Je clique sur le bouton "Se déconnecter" de la barre verticale. |
| **Then** | Je suis envoyé à la page Login. |

## Scénario 12
| | |
|---|---|
| **Given** | Je suis connecté en tant qu'administrateur et je suis sur la page Dashboard. |
| **When** | Je clique sur le bouton "Retour" en arrière de la navigation. |
| **Then** | Je reste sur la page Dashboard. |
