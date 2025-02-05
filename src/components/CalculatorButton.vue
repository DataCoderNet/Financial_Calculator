<template>
  <button
    :class="['calculator-button', type, { active: isActive }]"
    @click="$emit('click')"
    :aria-label="label"
  >
    {{ label }}
  </button>
</template>

<script>
export default {
  name: 'CalculatorButton',
  props: {
    // Label to display on the button
    label: {
      type: String,
      required: true
    },
    // Type of button: 'digit', 'operator', 'function', 'memory', 'fin'
    type: {
      type: String,
      default: 'digit',
      validator: (value) => ['digit', 'operator', 'function', 'memory', 'fin'].includes(value)
    },
    // Active state (for operators)
    isActive: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click']
}
</script>

<style scoped>
.calculator-button {
  width: 100%; /* Make button fill grid cell */
  min-width: 45px; /* Reduced from 60px */
  height: 45px; /* Reduced from 50px */
  margin: 0; /* Removed margin since we're using grid gap */
  border: none;
  border-radius: 5px;
  font-size: 1.1rem; /* Slightly reduced from 1.2rem */
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  user-select: none;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.calculator-button:active {
  transform: scale(0.95);
}

/* Digit buttons */
.calculator-button.digit {
  background-color: #f0f0f0;
  color: #333;
}

.calculator-button.digit:hover {
  background-color: #e0e0e0;
}

/* Operator buttons */
.calculator-button.operator {
  background-color: #ffa726;
  color: white;
  font-weight: bold; /* Added for better visibility */
}

.calculator-button.operator:hover,
.calculator-button.operator.active {
  background-color: #fb8c00;
}

/* Function buttons (clear, equals) */
.calculator-button.function {
  background-color: #e57373;
  color: white;
}

.calculator-button.function:hover {
  background-color: #ef5350;
}

/* Memory buttons */
.calculator-button.memory {
  background-color: #90caf9;
  color: white;
}

.calculator-button.memory:hover {
  background-color: #64b5f6;
}

/* FIN button */
.calculator-button.fin {
  background-color: #81c784;
  color: white;
}

.calculator-button.fin:hover {
  background-color: #66bb6a;
}
</style>