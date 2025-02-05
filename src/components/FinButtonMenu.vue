<template>
  <div class="fin-menu">
    <!-- Reuse CalculatorButton component for the FIN button -->
    <CalculatorButton
      label="FIN"
      type="fin"
      @click="toggleMenu"
    />
    <!-- Placeholder for future financial menu items -->
    <div v-if="isMenuOpen" class="menu-placeholder">
      Financial functions will be implemented in Phase 3
    </div>
  </div>
</template>

<script>
import CalculatorButton from './CalculatorButton.vue'

export default {
  name: 'FinButtonMenu',
  components: {
    CalculatorButton
  },
  data() {
    return {
      isMenuOpen: false
    }
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen
    }
  }
}
</script>

<style scoped>
.fin-menu {
  position: relative;
  display: inline-block;
  width: 100%; /* Take full width of container */
  max-width: 120px; /* Limit maximum width */
}

.fin-menu :deep(.calculator-button) {
  width: 100%;
  height: 40px; /* Slightly smaller than regular buttons */
}

.menu-placeholder {
  position: absolute;
  top: calc(100% + 5px);
  right: 0;
  background-color: #f5f5f5;
  padding: 8px;
  margin-top: 2px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  font-size: 0.85rem;
  color: #666;
  white-space: nowrap;
  z-index: 100;
}
</style>