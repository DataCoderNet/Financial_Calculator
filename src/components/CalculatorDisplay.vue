<template>
  <div class="calculator-display" :class="{ error: hasError }">
    <div class="display-content">
      {{ displayValue || '0' }}
    </div>
    <div v-if="hasError" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'CalculatorDisplay',
  props: {
    // Value to display
    value: {
      type: [Number, String],
      default: '0'
    },
    // Error message (if any)
    error: {
      type: String,
      default: ''
    }
  },
  computed: {
    hasError() {
      return Boolean(this.error)
    },
    displayValue() {
      if (this.hasError) return 'Error'
      return this.value
    }
  }
}
</script>

<style scoped>
.calculator-display {
  width: 100%;
  min-height: 65px; /* Reduced from 80px */
  background-color: #424242;
  border-radius: 8px; /* Reduced from 10px */
  margin-bottom: 15px; /* Reduced from 20px */
  padding: 8px 15px; /* Reduced from 10px 20px */
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}

.display-content {
  color: white;
  font-size: 2rem; /* Reduced from 2.5rem */
  font-family: 'Digital', monospace;
  text-align: right;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.error-message {
  color: #ff8a80;
  font-size: 0.875rem; /* Reduced from 1rem */
  text-align: right;
  margin-top: 4px; /* Reduced from 5px */
}

.calculator-display.error .display-content {
  color: #ff8a80;
}

/* Digital font effect */
@font-face {
  font-family: 'Digital';
  src: local('Courier New');
}
</style>