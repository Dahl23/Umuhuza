#!/usr/bin/env python3
"""
Script to generate UML and ER diagrams for the Umuhuza project report
"""

import os

# Output directory
OUTPUT_DIR = '/home/user_04/umuhuza/rapport/diagrams'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_class_diagram():
    """Generate comprehensive class diagram in PlantUML format"""

    plantuml = """@startuml umuhuza_class_diagram
!define ENTITY_COLOR #E1F5FE
!define ENUM_COLOR #FFF9C4

skinparam classAttributeIconSize 0
skinparam class {
    BackgroundColor ENTITY_COLOR
    BorderColor #0277BD
    ArrowColor #0277BD
}

' ========== USER PACKAGE ==========
package "users" {
    class User <<Entity>> {
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
        +email_verified_at: DateTimeField
        +phone_verified_at: DateTimeField
        +last_login: DateTimeField
        +date_joined: DateTimeField
        --
        +full_name(): String
        +roles(): List
        +primary_role(): String
    }

    class VerificationCode <<Entity>> {
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

    class UserBadge <<Entity>> {
        +userbadge_id: AutoField
        +userid: ForeignKey
        +badge_type: CharField
        +issuedat: DateTimeField
        +expires_at: DateTimeField
        --
        +is_active(): Boolean
    }

    class ActivityLog <<Entity>> {
        +log_id: AutoField
        +userid: ForeignKey
        +action_type: CharField
        +entity_type: CharField
        +entity_id: IntegerField
        +description: TextField
        +ip_address: GenericIPAddressField
        +user_agent: TextField
        +createdat: DateTimeField
    }
}

' ========== LISTINGS PACKAGE ==========
package "listings" {
    class Category <<Entity>> {
        +cat_id: AutoField
        +cat_name: CharField
        +slug: SlugField
        +cat_description: TextField
        +is_active: BooleanField
        +createdat: DateTimeField
        +updatedat: DateTimeField
    }

    class PricingPlan <<Entity>> {
        +pricing_id: AutoField
        +pricing_name: CharField
        +pricing_description: TextField
        +plan_price: DecimalField
        +duration_days: IntegerField
        +category_scope: CharField
        +max_listings: IntegerField
        +max_images_per_listing: IntegerField
        +is_featured: BooleanField
        +is_active: BooleanField
        +createdat: DateTimeField
        +updatedat: DateTimeField
    }

    class UserSubscription <<Entity>> {
        +subscription_id: AutoField
        +userid: ForeignKey
        +pricing_id: ForeignKey
        +subscription_status: CharField
        +listings_used: IntegerField
        +starts_at: DateTimeField
        +expires_at: DateTimeField
        +auto_renew: BooleanField
        +createdat: DateTimeField
        --
        +is_active(): Boolean
        +remaining_listings(): Integer
        +has_quota(): Boolean
    }

    class Listing <<Entity>> {
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
        +updatedat: DateTimeField
        --
        +increment_views(): void
    }

    class ListingImage <<Entity>> {
        +listimage_id: AutoField
        +listing_id: ForeignKey
        +image_url: CharField
        +is_primary: BooleanField
        +display_order: IntegerField
        +uploadedat: DateTimeField
    }

    class RatingReview <<Entity>> {
        +ratingrev_id: AutoField
        +userid: ForeignKey
        +reviewed_userid: ForeignKey
        +listing_id: ForeignKey
        +rating: IntegerField
        +comment: TextField
        +is_visible: BooleanField
        +createdat: DateTimeField
        +updatedat: DateTimeField
    }

    class Favorite <<Entity>> {
        +fav_id: AutoField
        +userid: ForeignKey
        +listing_id: ForeignKey
        +createdat: DateTimeField
    }

    class ReportMisconduct <<Entity>> {
        +reportmiscond_id: AutoField
        +userid: ForeignKey
        +reported_userid: ForeignKey
        +listing_id: ForeignKey
        +report_reason: TextField
        +report_type: CharField
        +report_status: CharField
        +admin_notes: TextField
        +createdat: DateTimeField
        +resolved_at: DateTimeField
    }
}

' ========== MESSAGING PACKAGE ==========
package "messaging" {
    class Chat <<Entity>> {
        +chat_id: AutoField
        +userid: ForeignKey
        +listing_id: ForeignKey
        +userid_as_seller: ForeignKey
        +last_message_at: DateTimeField
        +is_active: BooleanField
        +createdat: DateTimeField
    }

    class Message <<Entity>> {
        +message_id: AutoField
        +userid: ForeignKey
        +chat_id: ForeignKey
        +content: TextField
        +message_type: CharField
        +file_url: CharField
        +is_read: BooleanField
        +sentat: DateTimeField
        +read_at: DateTimeField
    }
}

' ========== NOTIFICATIONS PACKAGE ==========
package "notifications" {
    class Notification <<Entity>> {
        +notif_id: AutoField
        +userid: ForeignKey
        +notif_title: CharField
        +notif_message: TextField
        +notif_type: CharField
        +link_url: CharField
        +is_read: BooleanField
        +createdat: DateTimeField
        +read_at: DateTimeField
    }
}

' ========== PAYMENTS PACKAGE ==========
package "payments" {
    class Payment <<Entity>> {
        +payment_id: CharField
        +userid: ForeignKey
        +pricing_id: ForeignKey
        +listing_id: ForeignKey
        +payment_amount: DecimalField
        +payment_method: CharField
        +payment_status: CharField
        +payment_ref: CharField
        +transaction_id: CharField
        +failure_reason: TextField
        +createdat: DateTimeField
        +confirmed_at: DateTimeField
    }

    class DealerApplication <<Entity>> {
        +dealerapp_id: AutoField
        +userid: OneToOneField
        +business_name: CharField
        +business_type: CharField
        +business_address: TextField
        +business_phone: CharField
        +business_email: EmailField
        +tax_id: CharField
        +business_license: CharField
        +appli_status: CharField
        +rejection_reason: TextField
        +createdat: DateTimeField
        +approvedat: DateTimeField
        +updatedat: DateTimeField
    }

    class DealerDocument <<Entity>> {
        +dealerdoc_id: AutoField
        +dealerapp_id: ForeignKey
        +doc_type: CharField
        +file_url: CharField
        +file_size: IntegerField
        +verified: BooleanField
        +uploadedat: DateTimeField
    }
}

' ========== RELATIONSHIPS ==========

' User relationships
User "1" --> "0..*" VerificationCode : has
User "1" --> "0..*" UserBadge : earns
User "1" --> "0..*" ActivityLog : generates
User "1" --> "0..*" Listing : creates
User "1" --> "0..*" Favorite : favorites
User "1" --> "0..*" RatingReview : gives/receives
User "1" --> "0..*" Chat : participates
User "1" --> "0..*" Message : sends
User "1" --> "0..*" Notification : receives
User "1" --> "0..*" Payment : makes
User "1" --> "0..*" ReportMisconduct : submits/receives
User "1" --> "0..1" DealerApplication : submits
User "1" --> "0..*" UserSubscription : has

' Listing relationships
Category "1" --> "0..*" Listing : categorizes
Listing "1" --> "0..*" ListingImage : contains
Listing "1" --> "0..*" Favorite : favorited_by
Listing "1" --> "0..*" RatingReview : reviewed_in
Listing "1" --> "0..*" Chat : discussed_in
Listing "1" --> "0..*" ReportMisconduct : reported_in
Listing "1" --> "0..*" Payment : paid_for

' Subscription relationships
PricingPlan "1" --> "0..*" UserSubscription : includes
PricingPlan "1" --> "0..*" Payment : billed_in

' Messaging relationships
Chat "1" --> "0..*" Message : contains

' Dealer relationships
DealerApplication "1" --> "0..*" DealerDocument : includes

@enduml
"""

    with open(f'{OUTPUT_DIR}/class_diagram.puml', 'w') as f:
        f.write(plantuml)

    print("✓ Class diagram generated: class_diagram.puml")


def generate_er_diagram():
    """Generate Entity-Relationship diagram (MCD style)"""

    plantuml = """@startuml umuhuza_er_diagram
!define ENTITY_COLOR #E8F5E9
!define RELATIONSHIP_COLOR #FFF9C4

skinparam entity {
    BackgroundColor ENTITY_COLOR
    BorderColor #2E7D32
}

' ========== ENTITIES ==========

entity "USERS" as user {
    * USERID : INTEGER <<PK>>
    --
    * USER_FIRSTNAME : VARCHAR(255)
    * USER_LASTNAME : VARCHAR(255)
    * USER_EMAIL : VARCHAR(255) <<UNIQUE>>
    * PHONE_NUMBER : VARCHAR(20)
    USER_ROLE : VARCHAR(10)
    IS_SELLER : BOOLEAN
    IS_DEALER : BOOLEAN
    PROFILE_PHOTO : VARCHAR(255)
    IS_VERIFIED : BOOLEAN
    IS_ACTIVE : BOOLEAN
    EMAIL_VERIFIED : BOOLEAN
    PHONE_VERIFIED : BOOLEAN
    DATE_JOINED : TIMESTAMP
}

entity "VERIFICATION_CODES" as verif {
    * CODE_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * CODE : VARCHAR(10)
    * CODE_TYPE : VARCHAR(20)
    * CONTACT_INFO : VARCHAR(255)
    IS_USED : BOOLEAN
    EXPIRES_AT : TIMESTAMP
    CREATEDAT : TIMESTAMP
}

entity "USER_BADGES" as badge {
    * USERBADGE_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * BADGE_TYPE : VARCHAR(20)
    ISSUEDAT : TIMESTAMP
    EXPIRES_AT : TIMESTAMP
}

entity "ACTIVITY_LOGS" as log {
    * LOG_ID : INTEGER <<PK>>
    --
    USERID : INTEGER <<FK>>
    ACTION_TYPE : VARCHAR(100)
    ENTITY_TYPE : VARCHAR(50)
    ENTITY_ID : INTEGER
    DESCRIPTION : TEXT
    IP_ADDRESS : INET
    CREATEDAT : TIMESTAMP
}

entity "CATEGORIES" as category {
    * CAT_ID : INTEGER <<PK>>
    --
    * CAT_NAME : VARCHAR(255)
    * SLUG : VARCHAR(255) <<UNIQUE>>
    CAT_DESCRIPTION : TEXT
    IS_ACTIVE : BOOLEAN
    CREATEDAT : TIMESTAMP
}

entity "PRICING_PLANS" as pricing {
    * PRICING_ID : INTEGER <<PK>>
    --
    * PRICING_NAME : VARCHAR(255)
    PRICING_DESCRIPTION : TEXT
    * PLAN_PRICE : DECIMAL(12,2)
    * DURATION_DAYS : INTEGER
    CATEGORY_SCOPE : VARCHAR(20)
    MAX_LISTINGS : INTEGER
    MAX_IMAGES_PER_LISTING : INTEGER
    IS_FEATURED : BOOLEAN
    CREATEDAT : TIMESTAMP
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
    AUTO_RENEW : BOOLEAN
    CREATEDAT : TIMESTAMP
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
    VIEWS : INTEGER
    IS_FEATURED : BOOLEAN
    EXPIRATION_DATE : TIMESTAMP
    CREATEDAT : TIMESTAMP
}

entity "LISTING_IMAGES" as image {
    * LISTIMAGE_ID : INTEGER <<PK>>
    --
    * LISTING_ID : INTEGER <<FK>>
    * IMAGE_URL : VARCHAR(255)
    IS_PRIMARY : BOOLEAN
    DISPLAY_ORDER : INTEGER
    UPLOADEDAT : TIMESTAMP
}

entity "RATINGS_N_REVIEWS" as review {
    * RATINGREV_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * REVIEWED_USERID : INTEGER <<FK>>
    LISTING_ID : INTEGER <<FK>>
    * RATING : INTEGER
    COMMENT : TEXT
    IS_VISIBLE : BOOLEAN
    CREATEDAT : TIMESTAMP
}

entity "FAVORITES" as favorite {
    * FAV_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * LISTING_ID : INTEGER <<FK>>
    CREATEDAT : TIMESTAMP
}

entity "REPORTS_N_MISCONDUCT" as report {
    * REPORTMISCOND_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    REPORTED_USERID : INTEGER <<FK>>
    LISTING_ID : INTEGER <<FK>>
    * REPORT_REASON : TEXT
    REPORT_TYPE : VARCHAR(20)
    REPORT_STATUS : VARCHAR(10)
    ADMIN_NOTES : TEXT
    CREATEDAT : TIMESTAMP
}

entity "CHATS" as chat {
    * CHAT_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * LISTING_ID : INTEGER <<FK>>
    * USERID_AS_SELLER : INTEGER <<FK>>
    LAST_MESSAGE_AT : TIMESTAMP
    IS_ACTIVE : BOOLEAN
    CREATEDAT : TIMESTAMP
}

entity "MESSAGES" as message {
    * MESSAGE_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * CHAT_ID : INTEGER <<FK>>
    * CONTENT : TEXT
    MESSAGE_TYPE : VARCHAR(10)
    FILE_URL : VARCHAR(255)
    IS_READ : BOOLEAN
    SENTAT : TIMESTAMP
}

entity "NOTIFICATIONS" as notif {
    * NOTIF_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * NOTIF_TITLE : VARCHAR(255)
    * NOTIF_MESSAGE : TEXT
    NOTIF_TYPE : VARCHAR(20)
    LINK_URL : VARCHAR(255)
    IS_READ : BOOLEAN
    CREATEDAT : TIMESTAMP
}

entity "PAYMENTS" as payment {
    * PAYMENT_ID : VARCHAR(64) <<PK>>
    --
    * USERID : INTEGER <<FK>>
    * PRICING_ID : INTEGER <<FK>>
    LISTING_ID : INTEGER <<FK>>
    * PAYMENT_AMOUNT : DECIMAL(10,2)
    PAYMENT_METHOD : VARCHAR(20)
    PAYMENT_STATUS : VARCHAR(20)
    * PAYMENT_REF : VARCHAR(255) <<UNIQUE>>
    TRANSACTION_ID : VARCHAR(255)
    CREATEDAT : TIMESTAMP
}

entity "DEALER_APPLICATIONS" as dealer {
    * DEALERAPP_ID : INTEGER <<PK>>
    --
    * USERID : INTEGER <<FK>> <<UNIQUE>>
    * BUSINESS_NAME : VARCHAR(255)
    * BUSINESS_TYPE : VARCHAR(20)
    * BUSINESS_ADDRESS : TEXT
    BUSINESS_PHONE : VARCHAR(20)
    TAX_ID : VARCHAR(100)
    APPLI_STATUS : VARCHAR(10)
    CREATEDAT : TIMESTAMP
}

entity "DEALER_DOCUMENTS" as dealerdoc {
    * DEALERDOC_ID : INTEGER <<PK>>
    --
    * DEALERAPP_ID : INTEGER <<FK>>
    * DOC_TYPE : VARCHAR(255)
    * FILE_URL : VARCHAR(255)
    FILE_SIZE : INTEGER
    VERIFIED : BOOLEAN
    UPLOADEDAT : TIMESTAMP
}

' ========== RELATIONSHIPS ==========

user ||--o{ verif : "has"
user ||--o{ badge : "earns"
user ||--o{ log : "generates"
user ||--o{ subscription : "subscribes to"
user ||--o{ listing : "creates"
user ||--o{ favorite : "favorites"
user ||--o{ review : "gives/receives"
user ||--o{ chat : "participates"
user ||--o{ message : "sends"
user ||--o{ notif : "receives"
user ||--o{ payment : "makes"
user ||--o{ report : "submits/receives"
user ||--o| dealer : "applies as"

category ||--o{ listing : "categorizes"
pricing ||--o{ subscription : "used in"
pricing ||--o{ payment : "billed in"
subscription }o--|| user : "belongs to"
subscription }o--|| pricing : "uses"

listing }o--|| user : "created by"
listing }o--|| category : "belongs to"
listing ||--o{ image : "has"
listing ||--o{ favorite : "favorited in"
listing ||--o{ review : "reviewed in"
listing ||--o{ chat : "discussed in"
listing ||--o{ report : "reported in"
listing ||--o{ payment : "paid for"

chat }o--|| listing : "about"
chat ||--o{ message : "contains"

dealer ||--o{ dealerdoc : "includes"

@enduml
"""

    with open(f'{OUTPUT_DIR}/er_diagram.puml', 'w') as f:
        f.write(plantuml)

    print("✓ ER diagram generated: er_diagram.puml")


def generate_use_case_diagrams():
    """Generate use case diagrams for different actors"""

    plantuml = """@startuml umuhuza_use_cases
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

    ' ===== VISITOR USE CASES =====
    package "Fonctionnalités Publiques" {
        usecase "Consulter les annonces" as UC1
        usecase "Rechercher des annonces" as UC2
        usecase "Filtrer par catégorie" as UC3
        usecase "Filtrer par prix" as UC4
        usecase "Filtrer par localisation" as UC5
        usecase "Voir détails annonce" as UC6
        usecase "S'inscrire" as UC7
        usecase "Se connecter" as UC8
    }

    ' ===== BUYER USE CASES =====
    package "Fonctionnalités Acheteur" {
        usecase "Contacter vendeur" as UC10
        usecase "Ajouter aux favoris" as UC11
        usecase "Envoyer message" as UC12
        usecase "Consulter historique chats" as UC13
        usecase "Noter un vendeur" as UC14
        usecase "Signaler une annonce" as UC15
        usecase "Gérer profil" as UC16
        usecase "Vérifier email/téléphone" as UC17
    }

    ' ===== SELLER USE CASES =====
    package "Fonctionnalités Vendeur" {
        usecase "Créer une annonce" as UC20
        usecase "Modifier une annonce" as UC21
        usecase "Supprimer une annonce" as UC22
        usecase "Télécharger des photos" as UC23
        usecase "Gérer ses annonces" as UC24
        usecase "Consulter statistiques" as UC25
        usecase "Répondre aux messages" as UC26
        usecase "Acheter plan premium" as UC27
    }

    ' ===== DEALER USE CASES =====
    package "Fonctionnalités Dealer" {
        usecase "Soumettre candidature dealer" as UC30
        usecase "Télécharger documents" as UC31
        usecase "Créer annonces illimitées" as UC32
        usecase "Accéder au dashboard" as UC33
        usecase "Consulter analytics avancés" as UC34
        usecase "Gérer abonnement" as UC35
    }

    ' ===== ADMIN USE CASES =====
    package "Fonctionnalités Admin" {
        usecase "Gérer utilisateurs" as UC40
        usecase "Modérer annonces" as UC41
        usecase "Traiter signalements" as UC42
        usecase "Approuver candidatures dealer" as UC43
        usecase "Gérer catégories" as UC44
        usecase "Gérer plans tarifaires" as UC45
        usecase "Consulter logs activité" as UC46
        usecase "Bannir utilisateurs" as UC47
    }
}

' ===== VISITOR RELATIONSHIPS =====
visitor --> UC1
visitor --> UC2
visitor --> UC3
visitor --> UC4
visitor --> UC5
visitor --> UC6
visitor --> UC7
visitor --> UC8

' ===== BUYER RELATIONSHIPS =====
buyer --> UC10
buyer --> UC11
buyer --> UC12
buyer --> UC13
buyer --> UC14
buyer --> UC15
buyer --> UC16
buyer --> UC17

' ===== SELLER RELATIONSHIPS =====
seller --> UC20
seller --> UC21
seller --> UC22
seller --> UC23
seller --> UC24
seller --> UC25
seller --> UC26
seller --> UC27

' ===== DEALER RELATIONSHIPS =====
dealer --> UC30
dealer --> UC31
dealer --> UC32
dealer --> UC33
dealer --> UC34
dealer --> UC35

' ===== ADMIN RELATIONSHIPS =====
admin --> UC40
admin --> UC41
admin --> UC42
admin --> UC43
admin --> UC44
admin --> UC45
admin --> UC46
admin --> UC47

' ===== INCLUDE/EXTEND RELATIONSHIPS =====
UC20 ..> UC17 : <<include>>
UC27 ..> UC17 : <<require>>
UC30 ..> UC17 : <<require>>
UC10 ..> UC8 : <<require>>
UC12 ..> UC10 : <<include>>

@enduml
"""

    with open(f'{OUTPUT_DIR}/use_case_diagram.puml', 'w') as f:
        f.write(plantuml)

    print("✓ Use case diagram generated: use_case_diagram.puml")


def generate_sequence_diagrams():
    """Generate sequence diagrams for key workflows"""

    # 1. User Registration Sequence
    registration_seq = """@startuml user_registration_sequence
autonumber

actor "Utilisateur" as user
participant "Frontend\n(React)" as frontend
participant "Backend\nDjango API" as backend
database "PostgreSQL" as db
participant "Service\nEmail" as email

user -> frontend: Remplit formulaire inscription
frontend -> frontend: Valide données localement
frontend -> backend: POST /api/auth/register/\n(email, phone, password, ...)

backend -> backend: Valide données
backend -> db: Vérifie email unique
db --> backend: OK

backend -> db: Hash password (PBKDF2)
backend -> db: Crée User\n(is_verified=False)
db --> backend: User créé

backend -> backend: Génère code vérification
backend -> db: Sauvegarde VerificationCode
db --> backend: OK

backend -> email: Envoie email vérification
email --> backend: Email envoyé

backend --> frontend: 201 Created\n{user, tokens}
frontend --> user: Affiche page vérification

user -> frontend: Saisit code vérification
frontend -> backend: POST /api/auth/verify-email/\n{code}

backend -> db: Vérifie code valide
db --> backend: Code valide

backend -> db: Met à jour User\n(email_verified=True)
db --> backend: OK

backend -> db: Marque code utilisé
db --> backend: OK

backend --> frontend: 200 OK\n{success: true}
frontend --> user: Email vérifié ✓

@enduml
"""

    # 2. Create Listing Sequence
    create_listing_seq = """@startuml create_listing_sequence
autonumber

actor "Vendeur" as seller
participant "Frontend" as frontend
participant "Backend API" as backend
database "PostgreSQL" as db
participant "File Storage" as storage
participant "Notification\nService" as notif

seller -> frontend: Clique "Créer annonce"
frontend -> backend: GET /api/categories/
backend -> db: SELECT * FROM CATEGORIES
db --> backend: Liste catégories
backend --> frontend: 200 OK {categories}
frontend --> seller: Affiche formulaire

seller -> frontend: Remplit formulaire\n+ sélectionne photos
frontend -> frontend: Valide données

frontend -> backend: POST /api/listings/create/\n{title, description, price, ...}
backend -> backend: Vérifie authentification JWT
backend -> db: Vérifie quota utilisateur

alt Quota disponible
    backend -> db: INSERT INTO LISTINGS
    db --> backend: listing_id = 123

    loop Pour chaque photo
        frontend -> backend: POST /api/listings/123/upload-image/
        backend -> storage: Upload photo
        storage --> backend: image_url
        backend -> db: INSERT INTO LISTING_IMAGES
        db --> backend: OK
    end

    backend -> db: Met à jour is_seller=True
    db --> backend: OK

    backend -> notif: Crée notification admin\n"Nouvelle annonce à modérer"
    notif -> db: INSERT INTO NOTIFICATIONS

    backend --> frontend: 201 Created\n{listing}
    frontend --> seller: ✓ Annonce créée\n(en attente modération)

else Pas de quota
    backend --> frontend: 403 Forbidden\n"Quota dépassé"
    frontend --> seller: ⚠ Veuillez acheter un plan
end

@enduml
"""

    # 3. Messaging Sequence
    messaging_seq = """@startuml messaging_sequence
autonumber

actor "Acheteur" as buyer
participant "Frontend" as frontend
participant "Backend API" as backend
database "PostgreSQL" as db
participant "WebSocket\n(Future)" as ws
participant "Notification\nService" as notif

buyer -> frontend: Clique "Contacter vendeur"\nsur annonce #456
frontend -> backend: POST /api/chats/create/\n{listing_id: 456}

backend -> backend: Vérifie JWT token
backend -> db: SELECT seller FROM LISTINGS\nWHERE listing_id=456
db --> backend: seller_id = 789

backend -> db: SELECT * FROM CHATS WHERE\nbuyer=current_user AND\nlisting=456 AND seller=789

alt Chat existe déjà
    db --> backend: chat_id = 100
    backend --> frontend: 200 OK {chat_id: 100, existing: true}
else Nouveau chat
    backend -> db: INSERT INTO CHATS
    db --> backend: chat_id = 101
    backend --> frontend: 201 Created {chat_id: 101}
end

frontend -> backend: GET /api/chats/101/messages/
backend -> db: SELECT * FROM MESSAGES\nWHERE chat_id=101
db --> backend: messages[]
backend --> frontend: 200 OK {messages}
frontend --> buyer: Affiche interface chat

buyer -> frontend: Tape message\n"Disponible pour visite?"
frontend -> backend: POST /api/chats/101/messages/send/\n{content: "Disponible..."}

backend -> db: INSERT INTO MESSAGES
db --> backend: message_id = 500

backend -> db: UPDATE CHATS\nSET last_message_at=NOW()
db --> backend: OK

backend -> notif: Crée notification vendeur
notif -> db: INSERT INTO NOTIFICATIONS\n(type='chat')
db --> notif: OK

backend --> frontend: 201 Created {message}
frontend --> buyer: Message envoyé ✓

note over ws
  Dans version future:
  WebSocket push au vendeur
end note

@enduml
"""

    # 4. Payment Sequence
    payment_seq = """@startuml payment_sequence
autonumber

actor "Utilisateur" as user
participant "Frontend" as frontend
participant "Backend API" as backend
database "PostgreSQL" as db
participant "Payment Gateway\n(Lumicash)" as gateway
participant "Notification\nService" as notif

user -> frontend: Sélectionne plan premium
frontend -> backend: GET /api/pricing-plans/
backend -> db: SELECT * FROM PRICING_PLANS\nWHERE is_active=True
db --> backend: plans[]
backend --> frontend: 200 OK {plans}
frontend --> user: Affiche plans disponibles

user -> frontend: Choisit "Premium Plan"\n(10,000 BIF)
frontend -> backend: POST /api/payments/initiate/\n{pricing_id: 2, listing_id: 123}

backend -> backend: Vérifie JWT + listing ownership
backend -> backend: Génère payment_id unique
backend -> backend: Génère payment_ref unique

backend -> db: INSERT INTO PAYMENTS\n(status='pending')
db --> backend: OK

backend -> gateway: Initiate payment\n{amount, reference, callback_url}
gateway --> backend: {payment_url, transaction_id}

backend -> db: UPDATE PAYMENTS\nSET transaction_id=...
db --> backend: OK

backend --> frontend: 200 OK\n{payment_url, payment_id}
frontend --> user: Redirige vers Lumicash

user -> gateway: Complète paiement\n(Mobile Money)
gateway -> gateway: Traite paiement

gateway -> backend: POST /api/payments/callback/\n{transaction_id, status}

alt Paiement réussi
    backend -> db: UPDATE PAYMENTS\nSET status='successful'
    db --> backend: OK

    backend -> db: UPDATE LISTINGS\nSET is_featured=True,\nexpiration_date=NOW()+60days
    db --> backend: OK

    backend -> db: INSERT INTO USER_SUBSCRIPTIONS
    db --> backend: OK

    backend -> notif: Notification succès
    notif -> db: INSERT INTO NOTIFICATIONS

    backend --> gateway: 200 OK
    gateway --> user: Paiement confirmé ✓

else Paiement échoué
    backend -> db: UPDATE PAYMENTS\nSET status='failed',\nfailure_reason=...
    db --> backend: OK

    backend -> notif: Notification échec
    backend --> gateway: 200 OK
    gateway --> user: Paiement échoué ✗
end

user -> frontend: Retour au site
frontend -> backend: GET /api/payments/{payment_id}/
backend -> db: SELECT * FROM PAYMENTS\nWHERE payment_id=...
db --> backend: payment details
backend --> frontend: 200 OK {payment}
frontend --> user: Affiche statut paiement

@enduml
"""

    with open(f'{OUTPUT_DIR}/sequence_registration.puml', 'w') as f:
        f.write(registration_seq)

    with open(f'{OUTPUT_DIR}/sequence_create_listing.puml', 'w') as f:
        f.write(create_listing_seq)

    with open(f'{OUTPUT_DIR}/sequence_messaging.puml', 'w') as f:
        f.write(messaging_seq)

    with open(f'{OUTPUT_DIR}/sequence_payment.puml', 'w') as f:
        f.write(payment_seq)

    print("✓ Sequence diagrams generated:")
    print("  - sequence_registration.puml")
    print("  - sequence_create_listing.puml")
    print("  - sequence_messaging.puml")
    print("  - sequence_payment.puml")


def generate_architecture_diagrams():
    """Generate architecture and deployment diagrams"""

    # Component Diagram
    component_diagram = """@startuml architecture_components
!include <C4/C4_Component>

LAYOUT_WITH_LEGEND()

Container_Boundary(frontend, "Frontend Layer") {
    Component(react_app, "React Application", "React 18, Vite", "Interface utilisateur SPA")
    Component(router, "React Router", "react-router-dom", "Navigation et routing")
    Component(state, "State Management", "Context API", "Gestion état global")
    Component(api_client, "API Client", "Axios", "Communication avec backend")
}

Container_Boundary(backend, "Backend Layer") {
    Component(django, "Django Core", "Django 5.2", "Framework web principal")
    Component(drf, "Django REST Framework", "DRF 3.16", "API REST")
    Component(jwt_auth, "JWT Authentication", "SimpleJWT", "Authentification")
    Component(cors, "CORS Headers", "django-cors-headers", "Sécurité cross-origin")
    Component(imagekit, "Image Processing", "django-imagekit", "Traitement images")
}

Container_Boundary(apps, "Django Applications") {
    Component(users_app, "Users App", "Django App", "Gestion utilisateurs")
    Component(listings_app, "Listings App", "Django App", "Gestion annonces")
    Component(messaging_app, "Messaging App", "Django App", "Messagerie")
    Component(payments_app, "Payments App", "Django App", "Paiements")
    Component(notif_app, "Notifications App", "Django App", "Notifications")
}

ContainerDb(database, "PostgreSQL", "PostgreSQL 15+", "Base de données relationnelle")
Container(storage, "File Storage", "Local/S3", "Stockage fichiers")
Container_Ext(email, "Email Service", "SMTP/SendGrid", "Envoi emails")
Container_Ext(sms, "SMS Service", "Africa's Talking", "Envoi SMS")
Container_Ext(payment_gw, "Payment Gateway", "Lumicash", "Traitement paiements")

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

    # Deployment Diagram
    deployment_diagram = """@startuml deployment_diagram

node "Client Device" {
    artifact "Web Browser" as browser {
        component [React SPA] as spa
    }
}

node "Frontend Server\n(Vercel/Netlify)" as frontend_server {
    artifact "Static Assets" {
        component [HTML/CSS/JS] as static
        component [Images/Fonts] as assets
    }
}

node "Backend Server\n(Railway/DigitalOcean)" as backend_server {
    artifact "Application Server" {
        component [Gunicorn] as gunicorn
        component [Django Application] as django
    }
    artifact "WSGI" {
        component [uWSGI/Gunicorn Workers] as workers
    }
}

database "PostgreSQL Server\n(Managed Database)" as db_server {
    storage "Database" {
        artifact [umuhuza DB] as db
    }
}

cloud "CDN\n(Cloudflare)" as cdn {
    component [Static Cache] as cache
    component [DDoS Protection] as ddos
}

cloud "Object Storage\n(AWS S3/R2)" as object_storage {
    folder [User Uploads] as uploads
    folder [Listing Images] as images
    folder [Dealer Documents] as documents
}

node "External Services" {
    component [SendGrid\nEmail Service] as email
    component [Africa's Talking\nSMS Service] as sms
    component [Lumicash\nPayment Gateway] as payment
}

node "Monitoring & Logging" {
    component [Sentry\nError Tracking] as sentry
    component [Google Analytics] as analytics
}

' ===== CONNECTIONS =====

browser --> cdn : HTTPS
cdn --> frontend_server : HTTPS
cdn --> cache : Cache Hit

browser --> backend_server : API Requests\nHTTPS/REST
frontend_server --> backend_server : API Calls

backend_server --> db_server : PostgreSQL\nProtocol (5432)
backend_server --> object_storage : S3 API\nHTTPS
backend_server --> email : SMTP\nPort 587
backend_server --> sms : REST API
backend_server --> payment : REST API

backend_server --> sentry : Error Reports
browser --> analytics : Page Views

@enduml
"""

    # 3-Tier Architecture
    tier_architecture = """@startuml 3tier_architecture

package "Presentation Tier\n(Client-Side)" {
    [Web Browser] as browser
    [React Application] as react
    [Mobile App\n(Future)] as mobile
}

package "Application Tier\n(Server-Side)" {
    [Load Balancer\n(Nginx)] as lb
    [Django Application Server 1] as app1
    [Django Application Server 2] as app2
    [Celery Workers\n(Background Tasks)] as celery
    [Redis\n(Cache & Queue)] as redis
}

package "Data Tier\n(Storage)" {
    database "PostgreSQL\nMaster" as db_master
    database "PostgreSQL\nReplica (Read)" as db_replica
    storage "S3 Object Storage" as s3
}

package "External Services Tier" {
    [Email Gateway] as email
    [SMS Gateway] as sms
    [Payment Gateway] as payment
}

' ===== CONNECTIONS =====

browser --> react : Loads
react --> lb : API Requests\n(HTTPS)
mobile --> lb : API Requests\n(HTTPS)

lb --> app1 : Distributes
lb --> app2 : Distributes

app1 --> db_master : Write Operations
app1 --> db_replica : Read Operations
app2 --> db_master : Write Operations
app2 --> db_replica : Read Operations

app1 --> redis : Cache/Session
app2 --> redis : Cache/Session
app1 --> celery : Queue Tasks
app2 --> celery : Queue Tasks

celery --> redis : Get Tasks
celery --> db_master : Write

app1 --> s3 : Store/Retrieve Files
app2 --> s3 : Store/Retrieve Files

app1 --> email : Send Emails
app1 --> sms : Send SMS
app1 --> payment : Process Payments

db_master --> db_replica : Replication

@enduml
"""

    with open(f'{OUTPUT_DIR}/architecture_components.puml', 'w') as f:
        f.write(component_diagram)

    with open(f'{OUTPUT_DIR}/deployment_diagram.puml', 'w') as f:
        f.write(deployment_diagram)

    with open(f'{OUTPUT_DIR}/3tier_architecture.puml', 'w') as f:
        f.write(tier_architecture)

    print("✓ Architecture diagrams generated:")
    print("  - architecture_components.puml")
    print("  - deployment_diagram.puml")
    print("  - 3tier_architecture.puml")


def generate_activity_diagrams():
    """Generate activity diagrams for business processes"""

    # User Registration Activity
    registration_activity = """@startuml activity_registration
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
        :Email envoyé à l'utilisateur;
    fork again
        :SMS envoyé au téléphone;
    end fork

    :Utilisateur reçoit code;
    :Entre le code de vérification;

    if (Code valide?) then (oui)
        :Système marque email vérifié;
        :Système crée badge "Verified";
        :Log activité "USER_REGISTERED";
        :Utilisateur connecté automatiquement;
        :Redirection vers dashboard;
        stop
    else (non)
        :Affiche erreur "Code invalide";
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
    :Utilisateur corrige les erreurs;
    stop
endif

@enduml
"""

    # Listing Creation Activity
    listing_activity = """@startuml activity_create_listing
start

:Vendeur se connecte;

if (Email vérifié?) then (non)
    :Affiche message\n"Veuillez vérifier votre email";
    stop
else (oui)
endif

:Clique "Créer une annonce";

:Système vérifie quota;

if (Quota disponible?) then (oui)
    :Affiche formulaire création;

    partition "Saisie informations" {
        :Sélectionne catégorie;
        :Entre titre;
        :Entre description;
        :Entre prix;
        :Entre localisation;
        :Ajoute photos (min 1, max 10);
    }

    :Prévisualise l'annonce;

    if (Vendeur confirme?) then (oui)
        :Soumet l'annonce;

        fork
            :Système crée LISTING\n(status='pending');
        fork again
            :Upload photos vers S3;
        fork again
            :Crée LISTING_IMAGES;
        end fork

        :Met à jour is_seller=True;
        :Décrémente quota subscription;

        if (Plan premium?) then (oui)
            :Marque is_featured=True;
            :Définit expiration +60 jours;
        else (non)
            :Définit expiration +30 jours;
        endif

        fork
            :Notification à admin\n"Nouvelle annonce à modérer";
        fork again
            :Log activité "LISTING_CREATED";
        end fork

        :Affiche message succès\n"Annonce en attente de modération";
        stop

    else (non)
        :Retour au formulaire;
        stop
    endif

else (non)
    :Affiche message\n"Quota dépassé";
    :Propose plans premium;
    stop
endif

@enduml
"""

    # Payment Processing Activity
    payment_activity = """@startuml activity_payment
start

:Utilisateur choisit plan premium;

:Système affiche détails plan:
* Prix
* Durée
* Fonctionnalités;

:Utilisateur clique "Acheter";

if (Utilisateur connecté?) then (non)
    :Redirige vers login;
    stop
else (oui)
endif

:Système génère payment_id;
:Système crée record PAYMENT\n(status='pending');

:Système intègre Lumicash;
:Génère URL paiement;
:Redirige vers Lumicash;

:Utilisateur entre\ninformations paiement;

partition "Traitement Lumicash" {
    if (Paiement accepté?) then (oui)
        :Lumicash traite transaction;
        :Lumicash callback backend;
    else (non)
        :Callback échec;
        :UPDATE PAYMENT\nstatus='failed';
        :Notification utilisateur\n"Paiement échoué";
        stop
    endif
}

:Backend reçoit callback\nsuccès;

fork
    :UPDATE PAYMENT\nstatus='successful';
fork again
    :UPDATE LISTING\nis_featured=True;
fork again
    :CREATE USER_SUBSCRIPTION;
fork again
    :Notification utilisateur\n"Paiement confirmé";
fork again
    :Log activité\n"PAYMENT_COMPLETED";
end fork

:Redirige vers annonce;
:Affiche badge "Featured";

stop

@enduml
"""

    with open(f'{OUTPUT_DIR}/activity_registration.puml', 'w') as f:
        f.write(registration_activity)

    with open(f'{OUTPUT_DIR}/activity_create_listing.puml', 'w') as f:
        f.write(listing_activity)

    with open(f'{OUTPUT_DIR}/activity_payment.puml', 'w') as f:
        f.write(payment_activity)

    print("✓ Activity diagrams generated:")
    print("  - activity_registration.puml")
    print("  - activity_create_listing.puml")
    print("  - activity_payment.puml")


def generate_state_diagram():
    """Generate state diagram for listing states"""

    state_diagram = """@startuml listing_state_diagram
[*] --> Draft : Vendeur commence\nà créer annonce

Draft --> Pending : Vendeur soumet\nl'annonce

Pending --> Active : Admin approuve
Pending --> Rejected : Admin rejette
Pending --> Draft : Vendeur annule

Rejected --> Draft : Vendeur modifie

Active --> Sold : Vendeur marque\ncomme vendu
Active --> Expired : Date expiration\natteinte
Active --> Hidden : Vendeur cache\ntemporairement
Active --> Deleted : Vendeur/Admin\nsupprime

Hidden --> Active : Vendeur réactive

Expired --> Active : Vendeur renouvelle\n(paiement)
Expired --> Deleted : Auto-suppression\naprès 30 jours

Sold --> [*]
Deleted --> [*]
Rejected --> [*] : Après 90 jours

note right of Pending
  Modération admin requise
  pour toutes nouvelles annonces
end note

note right of Active
  Visible publiquement
  Indexée dans recherche
  Notifications actives
end note

note right of Expired
  Non visible publiquement
  Vendeur peut renouveler
  Auto-suppression si non renouvelé
end note

@enduml
"""

    with open(f'{OUTPUT_DIR}/state_listing.puml', 'w') as f:
        f.write(state_diagram)

    print("✓ State diagram generated: state_listing.puml")


# Main execution
if __name__ == '__main__':
    print("\n" + "="*60)
    print("GÉNÉRATION DES DIAGRAMMES UML - PROJET UMUHUZA")
    print("="*60 + "\n")

    print("Génération des diagrammes...\n")

    generate_class_diagram()
    generate_er_diagram()
    generate_use_case_diagrams()
    generate_sequence_diagrams()
    generate_architecture_diagrams()
    generate_activity_diagrams()
    generate_state_diagram()

    print("\n" + "="*60)
    print("✓ TOUS LES DIAGRAMMES ONT ÉTÉ GÉNÉRÉS AVEC SUCCÈS!")
    print("="*60)
    print(f"\nLes fichiers PlantUML (.puml) sont dans: {OUTPUT_DIR}")
    print("\nPour générer les images PNG:")
    print("1. Visitez: https://www.plantuml.com/plantuml/uml/")
    print("2. Copiez-collez le contenu de chaque fichier .puml")
    print("3. Téléchargez l'image PNG générée")
    print("\nOu utilisez PlantUML localement:")
    print("  java -jar plantuml.jar diagram.puml")
    print("\n")
