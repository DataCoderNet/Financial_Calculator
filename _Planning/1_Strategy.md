# Strategy for Building a Financial Calculator inspired in HP 17BII+

**Project Setup (Before Phase 1)**

* **Dependencies and Tools:** Python 3.8+, Node.js/npm or yarn, Code Editor (VS Code recommended), Git, Virtual Environment for Python (e.g., `venv`), Vite for Vue project setup, Postman (or similar API testing tool), Docker and Docker Compose (optional, for backend development and deployment consideration).
* **Version Control and Git Strategy:**
    * **Repository Setup:**
        * Initialize Git repository
        * Create and push to GitHub/similar platform
        * Set up main/master as the primary branch
    * **Branch Strategy:**
        * **main/master:** Production-ready code
        * **develop:** Main development branch, branches off from main
        * **Phase-specific branches:**
            * `phase1/calculator-ui`: Core calculator UI and basic arithmetic
            * `phase2/financial-api`: Financial functions backend
            * `phase3/fin-menus`: Financial function menus and parameter prompts
            * `phase4/memory-display`: Memory, display formatting, enhanced UI
            * `phase5/advanced-features`: Advanced features and polish
    * **Branch Workflow:**
        1. Create phase branch from `develop`
        2. Work on features within phase branch
        3. Once phase is complete and tested, merge into `develop`
        4. After thorough testing on `develop`, merge to `main` for release
    * **Additional Practices:** Use clear commit messages, utilize pull requests for code review, and maintain clean branch history

* **State Management Strategy:**
    * **Implementation:** Use Pinia (recommended over Vuex for Vue 3) for centralized state management
    * **Store Structure:**
        * **Calculator Store:**
            * Calculator mode (basic/financial)
            * Current display value
            * Operation history
            * Memory registers
        * **Financial Store:**
            * Current financial function
            * Parameter values
            * Results history
        * **UI Store:**
            * Menu states
            * Active prompts
            * Display formatting
        * **API Store:**
            * API request states
            * Loading states
            * Error handling
    * **Benefits:**
        * Centralized state management
        * Better component communication
        * Simplified testing
        * Improved maintainability

* **Testing Strategy:**
    * **Frontend Testing:**
        * **Framework:** Vitest + Vue Test Utils
        * **Coverage Areas:**
            * Unit tests for stores and utilities
            * Component tests for Vue components
            * Integration tests for component interactions
            * E2E tests using Cypress or Playwright
        * **Testing Practices:**
            * Test component rendering
            * Test user interactions
            * Test state management
            * Test API integrations
    * **Backend Testing:**
        * **Framework:** pytest with FastAPI TestClient
        * **Coverage Areas:**
            * Unit tests for calculation functions
            * API endpoint tests
            * Validation tests
            * Error handling tests
        * **Testing Practices:**
            * Use fixtures for common test data
            * Test edge cases
            * Test error conditions
            * Test API contracts

* **Deployment Strategy:**
    * **Development Environment:**
        * Local development setup with hot-reload
        * Environment-specific configuration
        * Docker Compose for local services
    * **CI/CD Pipeline:**
        * Automated testing on pull requests
        * Staging environment deployments
        * Production deployment workflow
    * **Production Architecture:**
        * Frontend deployed to CDN (e.g., Netlify, Vercel)
        * Backend containerized with Docker
        * API gateway configuration
        * CORS and security setup
    * **Monitoring and Maintenance:**
        * Error tracking
        * Performance monitoring
        * Usage analytics
        * Backup strategy

* **Documentation Strategy:**
    * **Inline Code Comments:**  Use clear and concise inline code comments throughout both frontend (Vue/JavaScript) and backend (Python) codebases for better understanding and maintainability.
    * **README Files:** Create README files for both the Frontend and Backend repositories. These should include: Project overview, setup instructions (how to run locally, dependencies), and any key architecture or design decisions.
    * **API Documentation:**  Leverage FastAPI's auto-generated API documentation (Swagger UI/ReDoc). This will be the primary documentation for backend API endpoints, request/response schemas, and usage.

**Core Menu Functions Definition**

* **FIN (Financial) Menu Functions:**
    * **TVM (Time Value of Money):**
        * N: Number of periods
        * I%YR: Annual interest rate
        * PV: Present value
        * PMT: Payment amount
        * FV: Future value
        * P/YR: Payments per year
        * BEGIN/END: Payment timing (start/end of period)
    * **ICNV (Interest Conversion):**
        * Nominal rate to effective rate conversion
        * Effective rate to nominal rate conversion
        * Different compounding periods (annual, semi-annual, quarterly, monthly, daily)
    * **CFLO (Cash Flow):**
        * NPV: Net Present Value
        * IRR: Internal Rate of Return
        * NFV: Net Future Value
        * Total: Sum of cash flows
    * **BOND:**
        * Bond price calculation
        * Yield to maturity
        * Accrued interest
        * Modified duration
    * **DEPRC (Depreciation):**
        * Straight-line depreciation
        * Declining balance
        * Sum-of-the-years'-digits
        * ACRS (Accelerated Cost Recovery System)
    * **BSCH (Business Schedules):**
        * Loan amortization schedules
        * Lease payment schedules
        * Investment analysis schedules

* **BUS (Business) Menu Functions:**
    * **%:**
        * Basic percentage calculations
        * Percentage of base number
        * Add percentage to base
    * **%Δ (Percentage Change):**
        * Percentage difference between two numbers
        * Percentage increase/decrease
        * Markup/markdown calculations
    * **MAR% (Margin Percentage):**
        * Cost to selling price calculations
        * Margin as percentage of cost
        * Margin as percentage of price
        * Markup calculations
    * **BRKEV (Break-Even Analysis):**
        * Fixed costs
        * Variable costs per unit
        * Selling price per unit
        * Break-even point in units
        * Break-even point in currency
    * **TIP% (Tip Calculator):**
        * Bill amount
        * Tip percentage
        * Split bill calculations
        * Total with tip
    * **CURRX (Currency Exchange):**
        * Currency conversion rates
        * Multiple currency calculations
        * Exchange rate updates
    * **UNITS (Unit Conversion):**
        * Length/Distance
        * Weight/Mass
        * Volume
        * Temperature
        * Area
        * Velocity

**Phase 1: Core Calculator UI and Basic Arithmetic Operations (Vue.js - Focus: UI Foundation & Core Interaction in Vue)**

* **Goals:**
    * **Introduce Vue.js and set up a basic Vue project using Vite.**
    * Build the fundamental HTML structure for the calculator UI **as Vue components**.  Specifically, plan to create components like:
        * `CalculatorDisplay.vue`: For the main calculator display area.
        * `CalculatorButton.vue`:  A generic and reusable component for all calculator buttons (digits, operators, functions, etc.).
        * `FinButtonMenu.vue`: For the "FIN" button and the financial function menu (initially, a placeholder).
    * Implement CSS styling **within Vue components or scoped styles** for a functional and recognizable calculator UI.
    * Use **Vue.js** to handle button clicks, implement basic arithmetic (+, -, *, /, =), and update the display area – all using Vue's reactivity and within Vue components.
    * Implement **basic error handling**, such as handling division by zero and displaying simple error messages in the UI.

* **Dependencies and Tools for Phase 1:** Vue.js, Vite, HTML, CSS.

* **Deliverables for Phase 1:**
    * A functional HTML calculator interface displayed in the browser, **built as Vue components (including `CalculatorDisplay.vue`, `CalculatorButton.vue`, `FinButtonMenu.vue`)**.
    * Basic CSS styling applied **within Vue components**.
    * Vue.js components implementing number input, +, -, *, /, = operations, and display updates **using Vue's reactivity**.
    * **Basic error handling** implemented for arithmetic operations (e.g., division by zero error message).
    * *No backend or database in this phase. All logic is client-side Vue.js for now.*

* **Testing and Iteration in Phase 1:**
    * Thoroughly test basic arithmetic operations for correctness within the Vue application. Include testing for basic error scenarios (e.g., division by zero).
    * Test UI responsiveness and button interactions within Vue components.
    * Get initial feedback on the UI layout and clarity of display in the Vue context.
    * **Iteration:** Based on testing and feedback, refine UI layout in Vue components, button placement, display logic (in Vue), arithmetic operation correctness in Vue, and basic error handling.

* **Estimated Timeline (Phase 1) - *Rough Estimate for Planning*:  1-2 weeks (To be refined after developer task estimation).**

---

**Phase 2: Financial Functions - Backend API (FastAPI) & Vue.js Frontend Interaction**

* **Goals:**
    * Set up the **FastAPI** backend API.
    * Define API endpoints in **FastAPI** for core financial functions (e.g., PV, FV, PMT, RATE, NPV, IRR - initially, focus on a few key TVM functions).
    * Implement financial calculation logic in Python using **`numpy-financial` library** (recommended) or implementing formulas directly, within **FastAPI route functions**.
    * Leverage **FastAPI's features for data validation and request/response handling using Pydantic models and type hints**.
    * **Vue.js frontend will interact with the FastAPI backend** using JavaScript `fetch` API within Vue components, to send requests, receive results, and update the UI.

* **Dependencies and Tools for Phase 2:** FastAPI, Uvicorn, Pydantic, Python (with `numpy-financial` or similar library), Postman (or similar API testing tool), JavaScript `fetch` API (in Vue).

* **Deliverables for Phase 2:**
    * Fully functional **FastAPI** backend API with endpoints for core financial calculations.
    * **FastAPI** API endpoints defined using Pydantic models for request/response data and type hints for validation.
    * **Vue.js frontend integrated with the FastAPI API** to send requests and display results from the backend for financial functions. API interaction implemented within Vue components using `fetch`.
    * Automatic API documentation generated by **FastAPI** (Swagger UI/ReDoc) for the financial function endpoints.
    * Basic testing of **FastAPI** API endpoints and Vue-FastAPI integration.

* **Testing and Iteration in Phase 2:**
    * Rigorously test the accuracy of financial calculations in Python within **FastAPI** backend against known formulas or existing financial calculators.
    * Test **FastAPI** API endpoints for correct input validation (using Pydantic), handling valid and invalid requests, and response structure. Use Postman or similar API testing tool for thorough endpoint testing.
    * Utilize the automatically generated **FastAPI API documentation** (Swagger UI/ReDoc) to test endpoints and understand API contracts.
    * Test the data flow between **Vue frontend (using `fetch`) and FastAPI API** for financial functions, ensuring correct requests are sent and responses are properly handled in Vue.
    * **Iteration:** Refine calculation logic in Python for accuracy, optimize **FastAPI** API endpoint design, improve data handling between Vue frontend and backend, enhance error handling and validation within **FastAPI** using Pydantic, refine API documentation based on testing, and improve Vue-FastAPI data exchange.

* **Estimated Timeline (Phase 2) - *Rough Estimate for Planning*: 2-3 weeks (To be refined after developer task estimation).**

---

**Phase 3: Implement Financial Function Menus and Parameter Prompts in Vue (Focus: Enhanced UI for Financial Functions within Vue)**

* **Goals:**
    * **Implement the "FIN" button menu structure in Vue:**
        * When "FIN" button is clicked, display a **menu of financial function *categories* within Vue components** (e.g., TVM, Loans, NPV/IRR).
        * When a category is selected, display a **sub-menu of *functions* within that category in Vue (e.g., PV, FV, PMT within TVM).**
    * **Implement the *parameter prompting* UI within the main display area in Vue:**
        * When a financial function (like PV) is selected from the menu:
            * **Clear the calculator display area in Vue.**
            * **Display prompts *in sequence* within the display area for each parameter of the selected function (e.g., "Enter Present Value (PV):", "Enter Interest Rate (%):", etc.) - using Vue's reactivity to manage prompts.**
            * Use input fields (or simulated input using number button clicks) for parameter entry within the prompts **in Vue**.
    * **Ensure the Vue frontend seamlessly interacts with the FastAPI backend API (from Phase 2) for the financial functions using the menu and parameter prompts.**

* **Dependencies and Tools for Phase 3:** Vue.js, HTML, CSS. (Potentially Vue UI Component Library choice could be made in this phase or Phase 4).

* **Deliverables for Phase 3:**
    * **Functional "FIN" menu structure implemented in Vue (categories and functions).**
    * **Parameter prompting UI implemented in Vue within the calculator display area.**
    * **Vue frontend integrated to send requests to FastAPI API based on function selection and parameter input through the new UI elements.**
    * CSS styling improved for the new menu and prompt UI elements within Vue components.

* **Testing and Iteration in Phase 3:**
    * Test the "FIN" menu navigation and function selection in Vue thoroughly.
    * Test the parameter prompting UI flow for each financial function within Vue components.
    * Verify data flow between Vue frontend parameter input (through the new UI) and **FastAPI API** endpoint calls.
    * Test correct display of results received from **FastAPI API** in Vue UI (parameter prompts and calculator display).
    * **Iteration:** Refine menu structure and navigation in Vue, improve parameter prompting UI clarity and usability in Vue, optimize Vue component structure, enhance Vue-FastAPI API integration within the menu/prompt flow, refine CSS styling for menus and prompts based on user feedback.

---

**Phase 4: Memory, Display Formatting & Enhanced Vue UI (Focus: Improving Usability & Leveraging Vue with FastAPI backend, with Vue-based UI)**

* **Goals:**
    * **Implement Memory registers (M+, M-, MR, MC) in Vue Components.**
    * **Implement number formatting for the display within Vue components.**
    * **Further enhance UI using Vue features:** Transitions, animations, input validation, menus.
    * **Potentially integrate a more feature-rich Vue UI Component Library to enhance the visual style and component set of the Vue UI.**

* **Dependencies and Tools for Phase 4:** Vue.js, HTML, CSS, (Potentially Vue UI Component Library - e.g., Vuetify, Element UI, if chosen).

* **Deliverables for Phase 4:**
    * Memory register functionality implemented in Vue components.
    * Number formatting implemented within Vue components.
    * Smoother UI transitions and animations added using Vue features.
    * Improved input handling and validation in Vue components.
    * Potentially enhanced visual style through Vue UI component library integration.

* **Testing and Iteration in Phase 4:**
    * Test memory register functionality within Vue context.
    * Verify number formatting correctly in Vue components.
    * Test UI transitions and animations within Vue UI.
    * User testing on usability enhancements of the Vue-based UI.
    * **Iteration:** Refine memory functions in Vue, adjust number formatting, improve transitions in Vue, optimize Vue component logic, customize UI component library styling (if integrated).

---

**Phase 5: Advanced Features, Polish, Testing/Deployment (Vue Enhanced UI, FastAPI Backend - Focus: Feature Completeness & Readying for Use - Full Stack Vue & FastAPI application)**

* **Goals:**
    * Implement more advanced financial functions (**using FastAPI backend API and Vue frontend interaction**).
    * Potentially implement "presets" or "templates" (**using SQLite with FastAPI and Vue UI**).
    * Further polish the Vue UI design, responsiveness, and accessibility.
    * Implement comprehensive testing (unit tests for Python **FastAPI** backend, component tests for Vue frontend, UI integration tests).
    * Prepare for deployment of the **Vue frontend and FastAPI backend** application stack, considering **Docker for backend deployment**.

* **Dependencies and Tools for Phase 5:** Vue.js, FastAPI, SQLite (if presets are implemented), Vue Test Utils (for component testing), pytest (for backend testing), Deployment platform (e.g., Heroku, Netlify, Vercel, AWS - consider platforms suitable for Docker if Docker deployment is chosen for backend). Docker (for backend deployment).

* **Deliverables for Phase 5:**
    * Implementation of advanced financial functions (**FastAPI API, Vue UI interaction**).
    * "Presets" feature (optional, **FastAPI backend + Vue UI + SQLite**).
    * Polished and responsive Vue UI design.
    * Comprehensive test suite covering **FastAPI** backend and Vue frontend components.
    * Deployment setup for the **Vue frontend and FastAPI backend stack**, potentially using **Docker for the FastAPI backend**.

* **Testing and Iteration in Phase 5:**
    * Thorough testing of all implemented combined backend (**FastAPI**) and Vue frontend features.
    * User acceptance testing with the Vue-based UI.
    * Performance testing of the complete Vue/**FastAPI** application.
    * Accessibility testing of the Vue frontend.
    * **Iteration:** Address remaining bugs in both Vue frontend and FastAPI backend, refine advanced features, finalize UI polish, optimize full-stack performance, prepare for final deployment.

