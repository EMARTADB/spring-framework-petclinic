# Component Inventory (UI)

Server-side JSP UI, no SPA framework.
- Views (`src/main/webapp/WEB-INF/jsp/`): `welcome`, `exception`, `owners/{findOwners,ownersList,ownerDetails,createOrUpdateOwnerForm}`, `pets/{createOrUpdatePetForm,createOrUpdateVisitForm}`, `vets/vetList`.
- Tag files (`WEB-INF/tags/`): layout (`layout`, `htmlHeader`, `bodyHeader`, `menu`, `menuItem`, `footer`, `pivotal`), form (`inputField`, `selectField`, `localDate`).
- Static: `webapp/resources/{css,scss,fonts}`; SCSS compiled via libsass-maven-plugin (`css` profile); Bootstrap via webjars.
