#!/usr/bin/env python3
"""
Script pour générer tous les diagrammes UML en FRANÇAIS - Projet Umuhuza
Diagrammes conformes au code réel après revue du codebase
"""

import os

OUTPUT_DIR = '/home/user_04/umuhuza/rapport/diagrams'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_class_diagram_fr():
    """Diagramme de classes en français"""

    plantuml = """@startuml diagramme_classes
!define ENTITY_COLOR #E1F5FE
!define ENUM_COLOR #FFF9C4

skinparam classAttributeIconSize 0
skinparam class {
    BackgroundColor ENTITY_COLOR
    BorderColor #0277BD
    ArrowColor #0277BD
}

' ========== PACKAGE USERS ==========
package "users" {
    class Utilisateur <<Entité>> {
        +userid: AutoField
        +user_firstname: CharField
        +user_lastname: CharField
        +email: EmailField
        +phone_number: CharField
        +user_role: CharField
        +is_seller: BooleanField
        +is_dealer: BooleanField
        +profile_photo: CharField
        +is_verified: BooleanField
        +is_active: BooleanField
        +email_verified: BooleanField
        +phone_verified: BooleanField
        +date_joined: DateTimeField
        --
        +full_name(): String
        +roles(): List
        +primary_role(): String
    }

    class CodeVerification <<Entité>> {
        +code_id: AutoField
        +userid: ForeignKey
        +code: CharField
        +code_type: CharField
        +contact_info: CharField
        +is_used: BooleanField
        +expires_at: DateTimeField
        +createdat: DateTimeField
        --
        +is_valid(): Boolean
    }

    class BadgeUtilisateur <<Entité>> {
        +userbadge_id: AutoField
        +userid: ForeignKey
        +badge_type: CharField
        +issuedat: DateTimeField
        +expires_at: DateTimeField
        --
        +is_active(): Boolean
    }

    class JournalActivite <<Entité>> {
        +log_id: AutoField
        +userid: ForeignKey
        +action_type: CharField
        +entity_type: CharField
        +entity_id: IntegerField
        +description: TextField
        +ip_address: GenericIPAddressField
        +createdat: DateTimeField
    }
}

' ========== PACKAGE LISTINGS ==========
package "listings" {
    class Categorie <<Entité>> {
        +cat_id: AutoField
        +cat_name: CharField
        +slug: SlugField
        +cat_description: TextField
        +is_active: BooleanField
        +createdat: DateTimeField
    }

    class PlanTarifaire <<Entité>> {
        +pricing_id: AutoField
        +pricing_name: CharField
        +pricing_description: TextField
        +plan_price: DecimalField
        +duration_days: IntegerField
        +category_scope: CharField
        +max_listings: IntegerField
        +max_images_per_listing: IntegerField
        +is_featured: BooleanField
        +createdat: DateTimeField
    }

    class AbonnementUtilisateur <<Entité>> {
        +subscription_id: AutoField
        +userid: ForeignKey
        +pricing_id: ForeignKey
        +subscription_status: CharField
        +listings_used: IntegerField
        +starts_at: DateTimeField
        +expires_at: DateTimeField
        +auto_renew: BooleanField
        --
        +is_active(): Boolean
        +remaining_listings(): Integer
        +has_quota(): Boolean
    }

    class Annonce <<Entité>> {
        +listing_id: AutoField
        +userid: ForeignKey
        +cat_id: ForeignKey
        +listing_title: CharField
        +list_description: TextField
        +listing_price: DecimalField
        +list_location: CharField
        +listing_status: CharField
        +views: IntegerField
        +is_featured: BooleanField
        +expiration_date: DateTimeField
        +createdat: DateTimeField
        --
        +increment_views(): void
    }

    class ImageAnnonce <<Entité>> {
        +listimage_id: AutoField
        +listing_id: ForeignKey
        +image_url: CharField
        +is_primary: BooleanField
        +display_order: IntegerField
        +uploadedat: DateTimeField
    }

    class NotationAvis <<Entité>> {
        +ratingrev_id: AutoField
        +userid: ForeignKey
        +reviewed_userid: ForeignKey
        +listing_id: ForeignKey
        +rating: IntegerField
        +comment: TextField
        +is_visible: BooleanField
        +createdat: DateTimeField
    }

    class Favori <<Entité>> {
        +fav_id: AutoField
        +userid: ForeignKey
        +listing_id: ForeignKey
        +createdat: DateTimeField
    }

    class Signalement <<Entité>> {
        +reportmiscond_id: AutoField
        +userid: ForeignKey
        +reported_userid: ForeignKey
        +listing_id: ForeignKey
        +report_reason: TextField
        +report_type: CharField
        +report_status: CharField
        +admin_notes: TextField
        +createdat: DateTimeField
    }
}

' ========== PACKAGE MESSAGING ==========
package "messaging" {
    class Conversation <<Entité>> {
        +chat_id: AutoField
        +userid: ForeignKey
        +listing_id: ForeignKey
        +userid_as_seller: ForeignKey
        +last_message_at: DateTimeField
        +is_active: BooleanField
        +createdat: DateTimeField
    }

    class Message <<Entité>> {
        +message_id: AutoField
        +userid: ForeignKey
        +chat_id: ForeignKey
        +content: TextField
        +message_type: CharField
        +file_url: CharField
        +is_read: BooleanField
        +sentat: DateTimeField
    }
}

' ========== PACKAGE NOTIFICATIONS ==========
package "notifications" {
    class Notification <<Entité>> {
        +notif_id: AutoField
        +userid: ForeignKey
        +notif_title: CharField
        +notif_message: TextField
        +notif_type: CharField
        +link_url: CharField
        +is_read: BooleanField
        +createdat: DateTimeField
    }
}

' ========== PACKAGE PAYMENTS ==========
package "payments" {
    class Paiement <<Entité>> {
        +payment_id: CharField
        +userid: ForeignKey
        +pricing_id: ForeignKey
        +listing_id: ForeignKey
        +payment_amount: DecimalField
        +payment_method: CharField
        +payment_status: CharField
        +payment_ref: CharField
        +transaction_id: CharField
        +createdat: DateTimeField
    }

    class CandidatureDealer <<Entité>> {
        +dealerapp_id: AutoField
        +userid: OneToOneField
        +business_name: CharField
        +business_type: CharField
        +business_address: TextField
        +business_phone: CharField
        +business_email: EmailField
        +tax_id: CharField
        +appli_status: CharField
        +createdat: DateTimeField
    }

    class DocumentDealer <<Entité>> {
        +dealerdoc_id: AutoField
        +dealerapp_id: ForeignKey
        +doc_type: CharField
        +file_url: CharField
        +file_size: IntegerField
        +verified: BooleanField
        +uploadedat: DateTimeField
    }
}

' ========== RELATIONS ==========

Utilisateur "1" --> "0..*" CodeVerification : possède
Utilisateur "1" --> "0..*" BadgeUtilisateur : obtient
Utilisateur "1" --> "0..*" JournalActivite : génère
Utilisateur "1" --> "0..*" Annonce : crée
Utilisateur "1" --> "0..*" Favori : favoritise
Utilisateur "1" --> "0..*" NotationAvis : donne/reçoit
Utilisateur "1" --> "0..*" Conversation : participe
Utilisateur "1" --> "0..*" Message : envoie
Utilisateur "1" --> "0..*" Notification : reçoit
Utilisateur "1" --> "0..*" Paiement : effectue
Utilisateur "1" --> "0..*" Signalement : soumet/reçoit
Utilisateur "1" --> "0..1" CandidatureDealer : soumet
Utilisateur "1" --> "0..*" AbonnementUtilisateur : a

Categorie "1" --> "0..*" Annonce : catégorise
Annonce "1" --> "0..*" ImageAnnonce : contient
Annonce "1" --> "0..*" Favori : favorisée_par
Annonce "1" --> "0..*" NotationAvis : évaluée_dans
Annonce "1" --> "0..*" Conversation : discutée_dans
Annonce "1" --> "0..*" Signalement : signalée_dans
Annonce "1" --> "0..*" Paiement : payée_pour

PlanTarifaire "1" --> "0..*" AbonnementUtilisateur : inclut
PlanTarifaire "1" --> "0..*" Paiement : facturé_dans

Conversation "1" --> "0..*" Message : contient

CandidatureDealer "1" --> "0..*" DocumentDealer : inclut

@enduml
"""

    with open(f'{OUTPUT_DIR}/diagramme_classes.puml', 'w', encoding='utf-8') as f:
        f.write(plantuml)

    print("✓ Diagramme de classes généré: diagramme_classes.puml")


def generate_er_diagram_fr():
    """Diagramme ER (MCD) en français"""

    plantuml = """@startuml diagramme_er
!define ENTITY_COLOR #E8F5E9

skinparam entity {
    BackgroundColor ENTITY_COLOR
    BorderColor #2E7D32
}

entity "USERS" as user {
    * USERID : INTEGER <<PK>>
    --
    * USER_EMAIL : VARCHAR(255) <<UNIQUE>>
    * USER_FIRSTNAME : VARCHAR(255)
    * USER_LASTNAME : VARCHAR(255)
    * PHONE_NUMBER : VARCHAR(20)
    USER_ROLE : VARCHAR(10)
    IS_SELLER : BOOLEAN
    IS_DEALER : BOOLEAN
    IS_VERIFIED : BOOLEAN
    EMAIL_VERIFIED : BOOLEAN
    DATE_JOINED : TIMESTAMP
}

entity "LISTINGS" as listing {
    * LISTING_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * CAT_ID : INTEGER <<FK>>
    * LISTING_TITLE : VARCHAR(255)
    * LIST_DESCRIPTION : TEXT
    * LISTING_PRICE : DECIMAL(15,2)
    * LIST_LOCATION : VARCHAR(255)
    LISTING_STATUS : VARCHAR(10)
    IS_FEATURED : BOOLEAN
    VIEWS : INTEGER
    EXPIRATION_DATE : TIMESTAMP
    CREATEDAT : TIMESTAMP
}

entity "CATEGORIES" as category {
    * CAT_ID : INTEGER <<PK>>
    --
    * CAT_NAME : VARCHAR(255)
    * SLUG : VARCHAR(255) <<UNIQUE>>
    CAT_DESCRIPTION : TEXT
    IS_ACTIVE : BOOLEAN
}

entity "LISTING_IMAGES" as image {
    * LISTIMAGE_ID : INTEGER <<PK>>
    --
    * LISTING_ID : INTEGER <<FK>>
    * IMAGE_URL : VARCHAR(255)
    IS_PRIMARY : BOOLEAN
    DISPLAY_ORDER : INTEGER
}

entity "PRICING_PLANS" as pricing {
    * PRICING_ID : INTEGER <<PK>>
    --
    * PRICING_NAME : VARCHAR(255)
    * PLAN_PRICE : DECIMAL(12,2)
    * DURATION_DAYS : INTEGER
    MAX_LISTINGS : INTEGER
    MAX_IMAGES_PER_LISTING : INTEGER
    IS_FEATURED : BOOLEAN
}

entity "USER_SUBSCRIPTIONS" as subscription {
    * SUBSCRIPTION_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * PRICING_ID : INTEGER <<FK>>
    SUBSCRIPTION_STATUS : VARCHAR(10)
    LISTINGS_USED : INTEGER
    STARTS_AT : TIMESTAMP
    EXPIRES_AT : TIMESTAMP
}

entity "CHATS" as chat {
    * CHAT_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * LISTING_ID : INTEGER <<FK>>
    * USERID_AS_SELLER : INTEGER <<FK>>
    LAST_MESSAGE_AT : TIMESTAMP
    IS_ACTIVE : BOOLEAN
}

entity "MESSAGES" as message {
    * MESSAGE_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * CHAT_ID : INTEGER <<FK>>
    * CONTENT : TEXT
    MESSAGE_TYPE : VARCHAR(10)
    IS_READ : BOOLEAN
    SENTAT : TIMESTAMP
}

entity "PAYMENTS" as payment {
    * PAYMENT_ID : VARCHAR(64) <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * PRICING_ID : INTEGER <<FK>>
    LISTING_ID : INTEGER <<FK>>
    * PAYMENT_AMOUNT : DECIMAL(10,2)
    PAYMENT_STATUS : VARCHAR(20)
    * PAYMENT_REF : VARCHAR(255) <<UNIQUE>>
}

entity "NOTIFICATIONS" as notif {
    * NOTIF_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * NOTIF_TITLE : VARCHAR(255)
    * NOTIF_MESSAGE : TEXT
    NOTIF_TYPE : VARCHAR(20)
    IS_READ : BOOLEAN
}

entity "FAVORITES" as favorite {
    * FAV_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * LISTING_ID : INTEGER <<FK>>
    CREATEDAT : TIMESTAMP
}

entity "RATINGS_N_REVIEWS" as review {
    * RATINGREV_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * REVIEWED_USERID : INTEGER <<FK>>
    LISTING_ID : INTEGER <<FK>>
    * RATING : INTEGER
    COMMENT : TEXT
}

' ========== RELATIONS ==========

user ||--o{ listing : "crée"
user ||--o{ subscription : "souscrit"
user ||--o{ favorite : "favoritise"
user ||--o{ review : "donne/reçoit"
user ||--o{ chat : "participe"
user ||--o{ message : "envoie"
user ||--o{ notif : "reçoit"
user ||--o{ payment : "effectue"

category ||--o{ listing : "catégorise"
listing ||--o{ image : "possède"
listing ||--o{ favorite : "favorisée_dans"
listing ||--o{ review : "évaluée_dans"
listing ||--o{ chat : "discutée_dans"

pricing ||--o{ subscription : "utilisé_dans"
pricing ||--o{ payment : "facturé_dans"

subscription }o--|| user : "appartient_à"
subscription }o--|| pricing : "utilise"

chat }o--|| listing : "concerne"
chat ||--o{ message : "contient"

@enduml
"""

    with open(f'{OUTPUT_DIR}/diagramme_er.puml', 'w', encoding='utf-8') as f:
        f.write(plantuml)

    print("✓ Diagramme ER généré: diagramme_er.puml")


def generate_use_case_diagram_fr():
    """Diagramme de cas d'utilisation en français"""

    plantuml = """@startuml diagramme_cas_utilisation
left to right direction

skinparam actorStyle awesome
skinparam packageStyle rectangle

actor "Visiteur" as visitor
actor "Acheteur" as buyer
actor "Vendeur" as seller
actor "Dealer" as dealer
actor "Administrateur" as admin

buyer -up-|> visitor
seller -up-|> buyer
dealer -up-|> seller

package "Système Umuhuza" {

    package "Fonctionnalités Publiques" {
        usecase "Consulter annonces" as UC1
        usecase "Rechercher annonces" as UC2
        usecase "Filtrer par catégorie" as UC3
        usecase "Filtrer par prix" as UC4
        usecase "Voir détails annonce" as UC5
        usecase "S'inscrire" as UC6
        usecase "Se connecter" as UC7
    }

    package "Fonctionnalités Acheteur" {
        usecase "Contacter vendeur" as UC10
        usecase "Ajouter aux favoris" as UC11
        usecase "Envoyer message" as UC12
        usecase "Noter vendeur" as UC13
        usecase "Signaler annonce" as UC14
        usecase "Gérer profil" as UC15
        usecase "Vérifier email/téléphone" as UC16
    }

    package "Fonctionnalités Vendeur" {
        usecase "Créer annonce" as UC20
        usecase "Modifier annonce" as UC21
        usecase "Supprimer annonce" as UC22
        usecase "Télécharger photos" as UC23
        usecase "Gérer ses annonces" as UC24
        usecase "Consulter statistiques" as UC25
        usecase "Marquer comme vendu" as UC26
        usecase "Acheter plan premium" as UC27
    }

    package "Fonctionnalités Dealer" {
        usecase "Soumettre candidature" as UC30
        usecase "Télécharger documents" as UC31
        usecase "Créer annonces illimitées" as UC32
        usecase "Accéder dashboard" as UC33
        usecase "Gérer abonnement" as UC34
    }

    package "Fonctionnalités Admin" {
        usecase "Gérer utilisateurs" as UC40
        usecase "Traiter signalements" as UC41
        usecase "Approuver dealers" as UC42
        usecase "Gérer catégories" as UC43
        usecase "Gérer plans tarifaires" as UC44
        usecase "Consulter logs" as UC45
    }
}

' VISITEUR
visitor --> UC1
visitor --> UC2
visitor --> UC3
visitor --> UC4
visitor --> UC5
visitor --> UC6
visitor --> UC7

' ACHETEUR
buyer --> UC10
buyer --> UC11
buyer --> UC12
buyer --> UC13
buyer --> UC14
buyer --> UC15
buyer --> UC16

' VENDEUR
seller --> UC20
seller --> UC21
seller --> UC22
seller --> UC23
seller --> UC24
seller --> UC25
seller --> UC26
seller --> UC27

' DEALER
dealer --> UC30
dealer --> UC31
dealer --> UC32
dealer --> UC33
dealer --> UC34

' ADMIN
admin --> UC40
admin --> UC41
admin --> UC42
admin --> UC43
admin --> UC44
admin --> UC45

' RELATIONS include/extend
UC20 ..> UC16 : <<require>>
UC27 ..> UC16 : <<require>>
UC30 ..> UC16 : <<require>>
UC10 ..> UC7 : <<require>>
UC12 ..> UC10 : <<include>>

@enduml
"""

    with open(f'{OUTPUT_DIR}/diagramme_cas_utilisation.puml', 'w', encoding='utf-8') as f:
        f.write(plantuml)

    print("✓ Diagramme de cas d'utilisation généré: diagramme_cas_utilisation.puml")


def generate_sequence_diagrams_fr():
    """Diagrammes de séquence en français"""

    # 1. Inscription
    registration_seq = """@startuml sequence_inscription
autonumber

actor "Utilisateur" as user
participant "Frontend\\n(React)" as frontend
participant "Backend\\nDjango API" as backend
database "PostgreSQL" as db
participant "Service\\nEmail" as email

user -> frontend: Remplit formulaire inscription
frontend -> frontend: Valide données localement
frontend -> backend: POST /api/auth/register/\\n(email, phone, password, ...)

backend -> backend: Valide données
backend -> db: Vérifie email unique
db --> backend: OK

backend -> db: Hash password (PBKDF2)
backend -> db: Crée User\\n(is_verified=False)
db --> backend: User créé

backend -> backend: Génère code vérification
backend -> db: Sauvegarde VerificationCode
db --> backend: OK

backend -> email: Envoie email vérification
email --> backend: Email envoyé

backend --> frontend: 201 Created\\n{user, tokens}
frontend --> user: Affiche page vérification

user -> frontend: Saisit code vérification
frontend -> backend: POST /api/auth/verify-email/\\n{code}

backend -> db: Vérifie code valide
db --> backend: Code valide

backend -> db: Met à jour User\\n(email_verified=True)
db --> backend: OK

backend --> frontend: 200 OK
frontend --> user: Email vérifié ✓

@enduml
"""

    # 2. Création annonce (CORRIGÉ - activation automatique)
    create_listing_seq = """@startuml sequence_creation_annonce
autonumber

actor "Vendeur" as seller
participant "Frontend" as frontend
participant "Backend API" as backend
database "PostgreSQL" as db
participant "Stockage\\nFichiers" as storage

seller -> frontend: Clique "Créer annonce"
frontend -> backend: GET /api/categories/
backend -> db: SELECT * FROM CATEGORIES
db --> backend: Liste catégories
backend --> frontend: 200 OK {categories}

seller -> frontend: Remplit formulaire\\n+ sélectionne photos
frontend -> backend: POST /api/listings/create/\\n{title, description, price, images}

backend -> backend: Vérifie authentification JWT
backend -> db: Vérifie abonnement actif

alt Abonnement actif avec quota
    backend -> db: Vérifie quota disponible
    db --> backend: Quota OK

    backend -> db: INSERT INTO LISTINGS\\n(status='pending')
    db --> backend: listing_id = 123

    ' ACTIVATION AUTOMATIQUE
    backend -> db: UPDATE LISTINGS\\nSET status='active',\\nexpiration_date=NOW()+duration
    db --> backend: OK

    backend -> db: UPDATE subscriptions\\nSET listings_used += 1
    db --> backend: OK

    loop Pour chaque photo (max selon plan)
        backend -> storage: Upload photo optimisée
        storage --> backend: image_url
        backend -> db: INSERT INTO LISTING_IMAGES
        db --> backend: OK
    end

    backend -> db: UPDATE users\\nSET is_seller=True
    db --> backend: OK

    backend --> frontend: 201 Created\\n{listing, status='active'}
    frontend --> seller: ✓ Annonce créée et activée!

else Pas de quota ou abonnement expiré
    backend --> frontend: 403 Forbidden\\n"Quota dépassé"
    frontend --> seller: ⚠ Veuillez souscrire un plan
end

@enduml
"""

    # 3. Messagerie
    messaging_seq = """@startuml sequence_messagerie
autonumber

actor "Acheteur" as buyer
participant "Frontend" as frontend
participant "Backend API" as backend
database "PostgreSQL" as db
participant "Service\\nNotification" as notif

buyer -> frontend: Clique "Contacter vendeur"\\nsur annonce #456
frontend -> backend: POST /api/chats/create/\\n{listing_id: 456}

backend -> backend: Vérifie JWT token
backend -> db: SELECT seller FROM LISTINGS\\nWHERE listing_id=456
db --> backend: seller_id = 789

backend -> db: SELECT * FROM CHATS WHERE\\nbuyer=user AND listing=456

alt Chat existe
    db --> backend: chat_id = 100
    backend --> frontend: 200 OK {chat_id: 100}
else Nouveau chat
    backend -> db: INSERT INTO CHATS
    db --> backend: chat_id = 101
    backend --> frontend: 201 Created {chat_id: 101}
end

frontend -> backend: GET /api/chats/101/messages/
backend -> db: SELECT * FROM MESSAGES
db --> backend: messages[]
backend --> frontend: 200 OK {messages}

buyer -> frontend: Tape message
frontend -> backend: POST /api/chats/101/messages/send/\\n{content: "..."}

backend -> db: INSERT INTO MESSAGES
db --> backend: message_id = 500

backend -> db: UPDATE CHATS\\nSET last_message_at=NOW()
db --> backend: OK

backend -> notif: Crée notification vendeur
notif -> db: INSERT INTO NOTIFICATIONS
db --> notif: OK

backend --> frontend: 201 Created {message}
frontend --> buyer: Message envoyé ✓

@enduml
"""

    # 4. Paiement
    payment_seq = """@startuml sequence_paiement
autonumber

actor "Utilisateur" as user
participant "Frontend" as frontend
participant "Backend API" as backend
database "PostgreSQL" as db
participant "Lumicash" as gateway
participant "Service\\nNotification" as notif

user -> frontend: Sélectionne plan premium
frontend -> backend: GET /api/pricing-plans/
backend -> db: SELECT * FROM PRICING_PLANS
db --> backend: plans[]
backend --> frontend: 200 OK {plans}

user -> frontend: Choisit "Premium Plan"
frontend -> backend: POST /api/payments/initiate/\\n{pricing_id: 2, listing_id: 123}

backend -> backend: Génère payment_id unique
backend -> db: INSERT INTO PAYMENTS\\n(status='pending')
db --> backend: OK

backend -> gateway: Initiate payment\\n{amount, reference}
gateway --> backend: {payment_url, transaction_id}

backend -> db: UPDATE PAYMENTS\\nSET transaction_id=...
db --> backend: OK

backend --> frontend: 200 OK {payment_url}
frontend --> user: Redirige vers Lumicash

user -> gateway: Complète paiement\\n(Mobile Money)
gateway -> gateway: Traite paiement

gateway -> backend: POST /api/payments/callback/\\n{transaction_id, status}

alt Paiement réussi
    backend -> db: UPDATE PAYMENTS\\nSET status='successful'
    db --> backend: OK

    backend -> db: UPDATE LISTINGS\\nSET is_featured=True
    db --> backend: OK

    backend -> db: INSERT INTO USER_SUBSCRIPTIONS
    db --> backend: OK

    backend -> notif: Notification succès
    notif -> db: INSERT INTO NOTIFICATIONS

    backend --> gateway: 200 OK
    gateway --> user: Paiement confirmé ✓

else Paiement échoué
    backend -> db: UPDATE PAYMENTS\\nSET status='failed'
    backend -> notif: Notification échec
    backend --> gateway: 200 OK
    gateway --> user: Paiement échoué ✗
end

@enduml
"""

    with open(f'{OUTPUT_DIR}/sequence_inscription.puml', 'w', encoding='utf-8') as f:
        f.write(registration_seq)

    with open(f'{OUTPUT_DIR}/sequence_creation_annonce.puml', 'w', encoding='utf-8') as f:
        f.write(create_listing_seq)

    with open(f'{OUTPUT_DIR}/sequence_messagerie.puml', 'w', encoding='utf-8') as f:
        f.write(messaging_seq)

    with open(f'{OUTPUT_DIR}/sequence_paiement.puml', 'w', encoding='utf-8') as f:
        f.write(payment_seq)

    print("✓ Diagrammes de séquence générés (4 fichiers)")


def generate_state_diagram_fr():
    """Diagramme d'états CORRIGÉ basé sur le code réel"""

    state_diagram = """@startuml diagramme_etats_annonce
[*] --> Brouillon : Vendeur commence\\nà créer

note right of Brouillon
  État temporaire pendant
  la saisie du formulaire
end note

Brouillon --> Active : Vendeur soumet\\n+ abonnement actif\\n(ACTIVATION AUTO)

note right of Active
  Activée AUTOMATIQUEMENT
  par le système d'abonnement.
  AUCUNE approbation admin!

  expiration_date = NOW() + duration
  is_seller = True
  subscription.listings_used += 1
end note

Active --> Vendue : Vendeur marque\\ncomme vendue

Active --> Masquee : Vendeur masque\\ntemporairement

Active --> Expiree : Date expiration\\natteinte (auto)

note right of Expiree
  Système expire automatiquement
  après expiration_date
  (durée selon plan tarifaire)
end note

Masquee --> Active : Vendeur réactive\\n(si quota dispo)

Expiree --> Active : Vendeur renouvelle\\n(nouveau paiement)

Active --> Supprimee : Vendeur/Admin\\nsupprime
Masquee --> Supprimee : Vendeur/Admin\\nsupprime
Expiree --> Supprimee : Auto-suppression\\naprès 90 jours

Vendue --> [*]
Supprimee --> [*]

note bottom
  États possibles: active, sold, hidden, expired
  Pas d'état "pending" car activation automatique!

  Règle clé (voir views.py ligne 148):
  listing.listing_status = 'active'  # Immédiat!
end note

@enduml
"""

    with open(f'{OUTPUT_DIR}/diagramme_etats_annonce.puml', 'w', encoding='utf-8') as f:
        f.write(state_diagram)

    print("✓ Diagramme d'états généré (CORRIGÉ): diagramme_etats_annonce.puml")


def generate_activity_diagrams_fr():
    """Diagrammes d'activité en français"""

    # 1. Inscription
    registration_activity = """@startuml activite_inscription
start

:Utilisateur visite le site;
:Clique sur "S'inscrire";

:Remplit formulaire inscription:
* Prénom/Nom
* Email
* Téléphone
* Mot de passe;

if (Données valides?) then (oui)
    :Soumet le formulaire;
    :Système crée compte utilisateur;
    :Système génère code vérification;
    :Système envoie email avec code;

    fork
        :Email envoyé;
    fork again
        :SMS envoyé (optionnel);
    end fork

    :Utilisateur reçoit code;
    :Entre le code de vérification;

    if (Code valide?) then (oui)
        :Système marque email vérifié;
        :Système crée badge "Verified";
        :Log activité "USER_REGISTERED";
        :Connexion automatique;
        :Redirection vers dashboard;
        stop
    else (non)
        :Affiche "Code invalide";
        if (Trop de tentatives?) then (oui)
            :Verrouille temporairement;
            stop
        else (non)
            :Permet nouvelle tentative;
            stop
        endif
    endif

else (non)
    :Affiche erreurs validation;
    stop
endif

@enduml
"""

    # 2. Création annonce (CORRIGÉ)
    listing_activity = """@startuml activite_creation_annonce
start

:Vendeur se connecte;

if (Email vérifié?) then (non)
    :Affiche "Vérifiez votre email";
    stop
else (oui)
endif

:Clique "Créer une annonce";

:Système vérifie abonnement actif;

if (Abonnement actif?) then (oui)
    :Système vérifie quota disponible;

    if (Quota disponible?) then (oui)
        :Affiche formulaire création;

        partition "Saisie informations" {
            :Sélectionne catégorie;
            :Entre titre, description;
            :Entre prix, localisation;
            :Ajoute photos (max selon plan);
        }

        :Prévisualise l'annonce;

        if (Vendeur confirme?) then (oui)
            :Soumet l'annonce;

            fork
                :Crée LISTING (status='pending');
            fork again
                :Upload photos optimisées vers S3;
            fork again
                :Crée LISTING_IMAGES;
            end fork

            ' ACTIVATION AUTOMATIQUE
            :==ACTIVATION AUTOMATIQUE==
            UPDATE status='active'
            SET expiration_date=NOW()+duration;

            :Incrémente subscription.listings_used;

            if (Première annonce?) then (oui)
                :Met à jour is_seller=True;
            endif

            :Log activité "LISTING_CREATED";

            :Affiche "Annonce créée et activée!";
            stop

        else (non)
            :Retour au formulaire;
            stop
        endif

    else (non - quota dépassé)
        :Affiche "Quota dépassé";
        :Propose plans premium;
        stop
    endif

else (non - pas d'abonnement)
    :Affiche "Aucun abonnement actif";
    :Redirige vers plans tarifaires;
    stop
endif

@enduml
"""

    # 3. Paiement
    payment_activity = """@startuml activite_paiement
start

:Utilisateur choisit plan premium;

:Système affiche détails plan;

:Utilisateur clique "Acheter";

if (Utilisateur connecté?) then (non)
    :Redirige vers login;
    stop
else (oui)
endif

:Système génère payment_id;
:Crée PAYMENT (status='pending');

:Intègre Lumicash;
:Génère URL paiement;
:Redirige vers Lumicash;

:Utilisateur entre\\ninformations paiement;

partition "Traitement Lumicash" {
    if (Paiement accepté?) then (oui)
        :Lumicash traite transaction;
        :Callback backend;
    else (non)
        :Callback échec;
        :UPDATE status='failed';
        :Notification échec;
        stop
    endif
}

:Backend reçoit callback succès;

fork
    :UPDATE PAYMENT status='successful';
fork again
    :UPDATE LISTING is_featured=True;
fork again
    :CREATE USER_SUBSCRIPTION;
fork again
    :Notification succès;
fork again
    :Log "PAYMENT_COMPLETED";
end fork

:Redirige vers annonce;
:Affiche badge "Featured";

stop

@enduml
"""

    with open(f'{OUTPUT_DIR}/activite_inscription.puml', 'w', encoding='utf-8') as f:
        f.write(registration_activity)

    with open(f'{OUTPUT_DIR}/activite_creation_annonce.puml', 'w', encoding='utf-8') as f:
        f.write(listing_activity)

    with open(f'{OUTPUT_DIR}/activite_paiement.puml', 'w', encoding='utf-8') as f:
        f.write(payment_activity)

    print("✓ Diagrammes d'activité générés (3 fichiers)")


def generate_architecture_diagrams_fr():
    """Diagrammes d'architecture en français"""

    # Composants
    component_diagram = """@startuml architecture_composants
!include <C4/C4_Component>

LAYOUT_WITH_LEGEND()

Container_Boundary(frontend, "Couche Frontend") {
    Component(react_app, "Application React", "React 18, Vite", "Interface utilisateur SPA")
    Component(router, "React Router", "react-router-dom", "Navigation et routing")
    Component(state, "Gestion État", "Context API", "État global application")
    Component(api_client, "Client API", "Axios", "Communication avec backend")
}

Container_Boundary(backend, "Couche Backend") {
    Component(django, "Django Core", "Django 5.2", "Framework web principal")
    Component(drf, "Django REST Framework", "DRF 3.16", "API REST")
    Component(jwt_auth, "Authentification JWT", "SimpleJWT", "Authentification")
    Component(cors, "CORS Headers", "django-cors-headers", "Sécurité cross-origin")
    Component(imagekit, "Traitement Images", "django-imagekit", "Optimisation images")
}

Container_Boundary(apps, "Applications Django") {
    Component(users_app, "App Users", "Django App", "Gestion utilisateurs")
    Component(listings_app, "App Listings", "Django App", "Gestion annonces")
    Component(messaging_app, "App Messaging", "Django App", "Messagerie")
    Component(payments_app, "App Payments", "Django App", "Paiements")
    Component(notif_app, "App Notifications", "Django App", "Notifications")
}

ContainerDb(database, "PostgreSQL", "PostgreSQL 15+", "Base de données relationnelle")
Container(storage, "Stockage Fichiers", "Local/S3", "Images et documents")
Container_Ext(email, "Service Email", "SMTP/SendGrid", "Envoi emails")
Container_Ext(sms, "Service SMS", "Africa's Talking", "Envoi SMS")
Container_Ext(payment_gw, "Passerelle Paiement", "Lumicash", "Traitement paiements")

Rel(react_app, api_client, "Utilise")
Rel(api_client, drf, "Requêtes HTTP/JSON", "REST API")
Rel(drf, django, "Construit sur")
Rel(drf, jwt_auth, "Utilise")
Rel(django, users_app, "Inclut")
Rel(django, listings_app, "Inclut")
Rel(django, messaging_app, "Inclut")
Rel(django, payments_app, "Inclut")
Rel(django, notif_app, "Inclut")

Rel(users_app, database, "Lit/Écrit")
Rel(listings_app, database, "Lit/Écrit")
Rel(messaging_app, database, "Lit/Écrit")
Rel(payments_app, database, "Lit/Écrit")
Rel(notif_app, database, "Lit/Écrit")

Rel(listings_app, storage, "Upload/Download")
Rel(users_app, email, "Envoie")
Rel(users_app, sms, "Envoie")
Rel(payments_app, payment_gw, "Intègre")

@enduml
"""

    # Déploiement
    deployment_diagram = """@startuml diagramme_deploiement

node "Appareil Client" {
    artifact "Navigateur Web" as browser {
        component [Application React SPA] as spa
    }
}

node "Serveur Frontend\\n(Vercel/Netlify)" as frontend_server {
    artifact "Assets Statiques" {
        component [HTML/CSS/JS] as static
        component [Images/Fonts] as assets
    }
}

node "Serveur Backend\\n(Railway/DigitalOcean)" as backend_server {
    artifact "Serveur Application" {
        component [Gunicorn] as gunicorn
        component [Application Django] as django
    }
}

database "Serveur PostgreSQL\\n(Base Managée)" as db_server {
    storage "Base de Données" {
        artifact [DB umuhuza] as db
    }
}

cloud "CDN\\n(Cloudflare)" as cdn {
    component [Cache Statique] as cache
    component [Protection DDoS] as ddos
}

cloud "Stockage Objets\\n(AWS S3/R2)" as object_storage {
    folder [Uploads Utilisateurs] as uploads
    folder [Images Annonces] as images
    folder [Documents Dealers] as documents
}

node "Services Externes" {
    component [SendGrid\\nService Email] as email
    component [Africa's Talking\\nService SMS] as sms
    component [Lumicash\\nPasserelle Paiement] as payment
}

node "Monitoring & Logging" {
    component [Sentry\\nTracking Erreurs] as sentry
    component [Google Analytics] as analytics
}

browser --> cdn : HTTPS
cdn --> frontend_server : HTTPS
cdn --> cache : Cache Hit

browser --> backend_server : Requêtes API\\nHTTPS/REST
frontend_server --> backend_server : Appels API

backend_server --> db_server : PostgreSQL\\nPort 5432
backend_server --> object_storage : S3 API\\nHTTPS
backend_server --> email : SMTP\\nPort 587
backend_server --> sms : REST API
backend_server --> payment : REST API

backend_server --> sentry : Rapports Erreurs
browser --> analytics : Vues Pages

@enduml
"""

    # Architecture 3-tiers
    tier_architecture = """@startuml architecture_3tiers

package "Couche Présentation\\n(Client)" {
    [Navigateur Web] as browser
    [Application React] as react
    [Application Mobile\\n(Future)] as mobile
}

package "Couche Application\\n(Serveur)" {
    [Load Balancer\\n(Nginx)] as lb
    [Serveur Django 1] as app1
    [Serveur Django 2] as app2
    [Workers Celery\\n(Tâches Arrière-Plan)] as celery
    [Redis\\n(Cache & Queue)] as redis
}

package "Couche Données\\n(Stockage)" {
    database "PostgreSQL\\nMaster" as db_master
    database "PostgreSQL\\nReplica (Lecture)" as db_replica
    storage "Stockage Objets S3" as s3
}

package "Services Externes" {
    [Passerelle Email] as email
    [Passerelle SMS] as sms
    [Passerelle Paiement] as payment
}

browser --> react : Charge
react --> lb : Requêtes API\\n(HTTPS)
mobile --> lb : Requêtes API\\n(HTTPS)

lb --> app1 : Distribue
lb --> app2 : Distribue

app1 --> db_master : Opérations Écriture
app1 --> db_replica : Opérations Lecture
app2 --> db_master : Opérations Écriture
app2 --> db_replica : Opérations Lecture

app1 --> redis : Cache/Session
app2 --> redis : Cache/Session
app1 --> celery : Met en File
app2 --> celery : Met en File

celery --> redis : Récupère Tâches
celery --> db_master : Écrit

app1 --> s3 : Stocke/Récupère
app2 --> s3 : Stocke/Récupère

app1 --> email : Envoie Emails
app1 --> sms : Envoie SMS
app1 --> payment : Traite Paiements

db_master --> db_replica : Réplication

@enduml
"""

    with open(f'{OUTPUT_DIR}/architecture_composants.puml', 'w', encoding='utf-8') as f:
        f.write(component_diagram)

    with open(f'{OUTPUT_DIR}/diagramme_deploiement.puml', 'w', encoding='utf-8') as f:
        f.write(deployment_diagram)

    with open(f'{OUTPUT_DIR}/architecture_3tiers.puml', 'w', encoding='utf-8') as f:
        f.write(tier_architecture)

    print("✓ Diagrammes d'architecture générés (3 fichiers)")


def generate_missing_diagrams_fr():
    """Générer les 6 diagrammes manquants en français"""

    # 1. Diagramme d'objets
    object_diagram = """@startuml diagramme_objets
title Diagramme d'Objets - Instances Concrètes

object "utilisateur1 : Utilisateur" as user1 {
    userid = 1
    email = "john@example.com"
    user_firstname = "John"
    user_lastname = "Doe"
    is_seller = True
    is_verified = True
    date_joined = "2025-01-15"
}

object "abonnement1 : AbonnementUtilisateur" as sub1 {
    subscription_id = 5
    subscription_status = "active"
    listings_used = 2
    starts_at = "2025-01-20"
    expires_at = "2025-02-19"
}

object "planPremium : PlanTarifaire" as plan1 {
    pricing_id = 2
    pricing_name = "Plan Premium"
    plan_price = 10000
    duration_days = 30
    max_listings = 5
    is_featured = True
}

object "annonce1 : Annonce" as listing1 {
    listing_id = 123
    listing_title = "Villa moderne à Bujumbura"
    listing_price = 150000000
    listing_status = "active"
    is_featured = True
    views = 245
    createdat = "2025-01-25"
}

object "categorie1 : Categorie" as cat1 {
    cat_id = 1
    cat_name = "Real Estate - Houses"
    slug = "real-estate-houses"
}

object "image1 : ImageAnnonce" as img1 {
    listimage_id = 1
    image_url = "/media/listings/123/photo1.jpg"
    is_primary = True
    display_order = 0
}

object "image2 : ImageAnnonce" as img2 {
    listimage_id = 2
    image_url = "/media/listings/123/photo2.jpg"
    is_primary = False
    display_order = 1
}

object "favori1 : Favori" as fav1 {
    fav_id = 10
    createdat = "2025-01-26"
}

object "acheteur1 : Utilisateur" as buyer1 {
    userid = 2
    email = "marie@example.com"
    user_firstname = "Marie"
    user_lastname = "Martin"
}

' Relations
user1 -- sub1 : "possède"
sub1 -- plan1 : "utilise"
user1 -- listing1 : "a créé"
listing1 -- cat1 : "appartient à"
listing1 -- img1 : "contient"
listing1 -- img2 : "contient"
buyer1 -- fav1 : "a favorisé"
fav1 -- listing1 : "pointe vers"

note right of listing1
  Annonce activée automatiquement
  lors de la création grâce à
  l'abonnement actif du vendeur.

  Pas d'approbation admin requise!
end note

note bottom of sub1
  L'utilisateur a utilisé 2 sur 5
  annonces disponibles dans son
  plan Premium actif.
end note

@enduml
"""

    # 2. Diagramme de packages
    package_diagram = """@startuml diagramme_packages
!define PACKAGE_COLOR #E3F2FD
!define APP_COLOR #FFF9C4

skinparam package {
    BackgroundColor PACKAGE_COLOR
    BorderColor #1976D2
    FontStyle bold
}

package "backend" {

    package "umuhuza_api" <<Configuration>> #FFFFFF {
        [settings.py]
        [urls.py]
        [wsgi.py]
        [middleware.py]
    }

    package "users" <<App Django>> #APP_COLOR {
        [models.py]
        [views.py]
        [serializers.py]
        [urls.py]
        [admin.py]
        [utils.py]
    }

    package "listings" <<App Django>> #APP_COLOR {
        [models.py]
        [views.py]
        [serializers.py]
        [urls.py]
        [filters.py]
        [admin.py]
    }

    package "messaging" <<App Django>> #APP_COLOR {
        [models.py]
        [views.py]
        [serializers.py]
        [urls.py]
        [admin.py]
    }

    package "notifications" <<App Django>> #APP_COLOR {
        [models.py]
        [views.py]
        [serializers.py]
        [urls.py]
        [utils.py]
    }

    package "payments" <<App Django>> #APP_COLOR {
        [models.py]
        [views.py]
        [serializers.py]
        [urls.py]
        [lumicash.py]
    }

    package "media" <<Stockage>> #E8F5E9 {
        folder "listings/"
        folder "profiles/"
        folder "documents/"
    }
}

package "frontend" {
    package "src" {
        package "components" {
            folder "common/"
            folder "layout/"
            folder "listings/"
            folder "auth/"
        }

        package "pages" {
            [HomePage.tsx]
            [ListingsPage.tsx]
            [ProfilePage.tsx]
        }

        package "services" {
            [api.ts]
            [authService.ts]
            [listingsService.ts]
        }

        package "context" {
            [AuthContext.tsx]
            [NotificationContext.tsx]
        }
    }
}

' Dépendances
umuhuza_api ..> users : "inclut"
umuhuza_api ..> listings : "inclut"
umuhuza_api ..> messaging : "inclut"
umuhuza_api ..> notifications : "inclut"
umuhuza_api ..> payments : "inclut"

listings ..> users : "dépend de"
messaging ..> users : "dépend de"
messaging ..> listings : "dépend de"
notifications ..> users : "dépend de"
payments ..> users : "dépend de"
payments ..> listings : "dépend de"

listings ..> media : "utilise"

frontend ..> backend : "consomme API REST"

note right of umuhuza_api
  Package racine Django
  Configuration globale
  Routing principal
end note

note bottom of listings
  Package le plus important
  Gestion complète des annonces
  avec abonnements et activation auto
end note

@enduml
"""

    # 3. Diagramme de structure composite
    composite_diagram = """@startuml diagramme_structure_composite
title Diagramme de Structure Composite - Système d'Annonce

component "SystèmeAnnonce" {

    component "GestionAnnonce" {
        port "API REST" as api_port

        component "ValidateurDonnées" {
            [Validation Titre]
            [Validation Prix]
            [Validation Localisation]
        }

        component "GestionnaireImages" {
            [Optimiseur Images]
            [Stockage S3]
            [Générateur Miniatures]
        }

        component "VérificateurAbonnement" {
            [Vérif Quota]
            [Vérif Expiration]
            [Calcul Remaining]
        }

        component "ActivateurAutomatique" <<Clé>> {
            [Définir Statut Active]
            [Calculer Date Expiration]
            [Incrémenter Usage]
        }
    }

    component "GestionUtilisateur" {
        [Authentification JWT]
        [Vérification Email]
        [Gestion Rôles]
    }

    component "GestionFichiers" {
        [Upload]
        [Compression]
        [Validation Type]
    }

    component "BaseDonnées" {
        database "PostgreSQL" as db
    }
}

api_port --> ValidateurDonnées : "valide données"
ValidateurDonnées --> VérificateurAbonnement : "vérifie quota"
VérificateurAbonnement --> ActivateurAutomatique : "si OK, active"
ActivateurAutomatique --> db : "UPDATE status='active'"
GestionnaireImages --> GestionFichiers : "utilise"
GestionFichiers --> db : "sauvegarde URLs"

GestionUtilisateur --> GestionAnnonce : "authentifie"

note right of ActivateurAutomatique
  Composant clé du système!
  Active automatiquement
  les annonces après création
  sans intervention humaine.

  Code: views.py ligne 148
end note

note bottom of VérificateurAbonnement
  Vérifie:
  1. Abonnement actif?
  2. Quota disponible?
  3. Pas expiré?

  Si OK → activation automatique
  Si KO → erreur 403
end note

@enduml
"""

    # 4. Diagramme de communication
    communication_diagram = """@startuml diagramme_communication
title Diagramme de Communication - Création d'Annonce

actor "Vendeur" as seller
participant ":Frontend" as frontend
participant ":ListingView" as view
participant ":Subscription" as subscription
participant ":Listing" as listing
participant ":Storage" as storage
database ":Database" as db

seller -> frontend : 1: créerAnnonce(données)
frontend -> view : 2: POST /api/listings/create/

view -> subscription : 3: vérifierQuota(user)
subscription -> db : 3.1: SELECT quota
db -> subscription : 3.2: quota OK

view -> listing : 4: créer(données)
listing -> db : 4.1: INSERT (status='pending')
db -> listing : 4.2: listing_id

view -> listing : 5: activerAutomatiquement()
listing -> db : 5.1: UPDATE status='active'

view -> storage : 6: uploadImages(files)
storage -> db : 6.1: INSERT images

view -> subscription : 7: incrémenterUsage()
subscription -> db : 7.1: UPDATE listings_used

view -> frontend : 8: 201 Created {listing}
frontend -> seller : 9: "Annonce activée!"

note right of listing
  Communication 5:
  Activation automatique!
  Pas de modération admin.
end note

@enduml
"""

    # 5. Diagramme de temporisation
    timing_diagram = """@startuml diagramme_temporisation
title Diagramme de Temporisation - Cycle de Vie Annonce

concise "Annonce" as listing
concise "Abonnement" as subscription
concise "Système" as system

@0
listing is Brouillon
subscription is Actif
system is EnAttente

@5
listing is Active
note bottom: Activation AUTO immédiate\\naprès soumission formulaire

@10
system is SurveillanceExpiration
note bottom: Cron vérifie expiration_date

@30
listing is Active
subscription is Actif
note bottom: Annonce toujours active\\nsi avant expiration_date

@60
subscription is Expiré
note bottom: expiration_date atteinte

@61
system is TraitementExpiration
listing is Expiree
note bottom: Système marque comme expirée

@90
system is NettoyageAuto
note bottom: 30 jours après expiration

@91
listing is Supprimee
note bottom: Auto-suppression\\nsi pas renouvelée

highlight 0 to 5 #LightGreen : Création
highlight 5 to 60 #LightBlue : Période Active
highlight 60 to 61 #Orange : Expiration
highlight 61 to 90 #Yellow : Grâce 30j
highlight 90 to 91 #Red : Suppression

@enduml
"""

    # 6. Diagramme d'interaction global
    interaction_diagram = """@startuml diagramme_interaction_global
title Diagramme d'Interaction Global - Transaction Complète

start

:Utilisateur s'inscrit;

ref over : Séquence: Inscription
  - Création compte
  - Vérification email
  - Génération tokens JWT
end ref

:Utilisateur connecté;

partition "Gestion Abonnement" {
    :Consulte plans tarifaires;

    if (Choisit plan payant?) then (oui)
        ref over : Séquence: Paiement
          - Initialisation Lumicash
          - Traitement paiement
          - Création abonnement
        end ref

        :Abonnement actif créé;
    else (non)
        :Utilise plan gratuit (1 annonce);
    endif
}

partition "Création Annonce" {
    :Vendeur crée annonce;

    ref over : Activité: Création Annonce
      - Vérification quota
      - Upload images
      - ACTIVATION AUTOMATIQUE
      - Incrémentation usage
    end ref

    :Annonce publiée (active);
}

partition "Interactions Acheteur" {
    :Acheteur consulte annonces;

    fork
        :Ajoute aux favoris;
    fork again
        :Contacte vendeur;

        ref over : Séquence: Messagerie
          - Création conversation
          - Envoi messages
          - Notifications
        end ref
    end fork

    :Transaction réussie;
}

partition "Finalisation" {
    :Vendeur marque comme vendue;

    ref over : États: Annonce
      active → vendue
    end ref

    :Quota libéré;
}

stop

legend right
  Ce diagramme combine:
  - 4 diagrammes de séquence
  - 3 diagrammes d'activité
  - 1 diagramme d'états

  Montre le flux complet
  d'une transaction Umuhuza
endlegend

@enduml
"""

    # Écrire tous les fichiers
    with open(f'{OUTPUT_DIR}/diagramme_objets.puml', 'w', encoding='utf-8') as f:
        f.write(object_diagram)

    with open(f'{OUTPUT_DIR}/diagramme_packages.puml', 'w', encoding='utf-8') as f:
        f.write(package_diagram)

    with open(f'{OUTPUT_DIR}/diagramme_structure_composite.puml', 'w', encoding='utf-8') as f:
        f.write(composite_diagram)

    with open(f'{OUTPUT_DIR}/diagramme_communication.puml', 'w', encoding='utf-8') as f:
        f.write(communication_diagram)

    with open(f'{OUTPUT_DIR}/diagramme_temporisation.puml', 'w', encoding='utf-8') as f:
        f.write(timing_diagram)

    with open(f'{OUTPUT_DIR}/diagramme_interaction_global.puml', 'w', encoding='utf-8') as f:
        f.write(interaction_diagram)

    print("✓ Diagrammes manquants générés (6 fichiers):")
    print("  - diagramme_objets.puml")
    print("  - diagramme_packages.puml")
    print("  - diagramme_structure_composite.puml")
    print("  - diagramme_communication.puml")
    print("  - diagramme_temporisation.puml")
    print("  - diagramme_interaction_global.puml")


# EXÉCUTION PRINCIPALE
if __name__ == '__main__':
    print("\n" + "="*70)
    print("GÉNÉRATION DIAGRAMMES UML COMPLETS EN FRANÇAIS - PROJET UMUHUZA")
    print("Basés sur revue complète du codebase")
    print("="*70 + "\n")

    print("Génération des diagrammes...\n")

    generate_class_diagram_fr()
    generate_er_diagram_fr()
    generate_use_case_diagram_fr()
    generate_sequence_diagrams_fr()
    generate_state_diagram_fr()
    generate_activity_diagrams_fr()
    generate_architecture_diagrams_fr()
    generate_missing_diagrams_fr()

    print("\n" + "="*70)
    print("✓ TOUS LES DIAGRAMMES GÉNÉRÉS AVEC SUCCÈS!")
    print("="*70)
    print(f"\nFichiers PlantUML (.puml) dans: {OUTPUT_DIR}")
    print("\n📊 TOTAL: 20 diagrammes UML en français")
    print("\nPour générer les images PNG:")
    print("1. Visitez: https://www.plantuml.com/plantuml/uml/")
    print("2. Copiez-collez le contenu de chaque fichier .puml")
    print("3. Téléchargez l'image PNG générée")
    print("\n✅ Corrections appliquées:")
    print("  - Diagramme d'états: activation automatique (pas d'approbation admin)")
    print("  - Séquence création: activation immédiate basée sur abonnement")
    print("  - Activité création: flux correct avec activation auto")
    print("  - 6 diagrammes manquants ajoutés")
    print("  - Tout en français!")
    print("\n")
