<!-- Keep template and script sections exactly as they were, only updating the calculator width -->
<style>
body {
  margin: 0;
  padding: 2rem;
  min-width: 320px;
  min-height: 100vh;
  background-color: #f0f0f0;
}

#app {
  margin: 0 auto;
  text-align: center;
}

.app-container {
  position: relative;
  width: fit-content;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding-top: 2rem;
}

.calculator {
  background-color: #ffffff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 380px; /* Increased from 320px to accommodate wider parameter section */
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 2rem;
  gap: 12px;
}

/* Controls section - everything except display */
.controls-section {
  display: grid;
  grid-template-rows: 50px 40px 300px; /* Fixed heights: memory, fin, calculator grid */
  gap: 12px;
  margin-top: 12px;
}

.memory-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding: 8px;
}

.fin-section {
  display: flex;
  justify-content: flex-start;
  padding: 0 8px;
}

.calculator-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(5, 1fr);
  gap: 8px;
  padding: 8px;
}

.span-2 {
  grid-column: span 2;
}
</style>
