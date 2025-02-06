<template>
  <button
    :class="['calculator-button', type, { active: isActive }]"
    @click="handleClick"
    @mousedown="startRipple"
    :aria-label="label"
    ref="button"
  >
    {{ label }}
    <span v-if="rippleStyle" class="ripple" :style="rippleStyle"></span>
  </button>
</template>

<script>
export default {
  name: 'CalculatorButton',
  data() {
    return {
      rippleStyle: null
    }
  },
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
  methods: {
    handleClick(event) {
      this.$emit('click')
    },
    startRipple(event) {
      const button = this.$refs.button
      const rect = button.getBoundingClientRect()
      const size = Math.max(rect.width, rect.height)
      const x = event.clientX - rect.left - size / 2
      const y = event.clientY - rect.top - size / 2

      this.rippleStyle = {
        top: y + 'px',
        left: x + 'px',
        width: size + 'px',
        height: size + 'px'
      }

      // Remove ripple after animation
      setTimeout(() => {
        this.rippleStyle = null
      }, 1000)
    }
  },
  emits: ['click']
}
</script>

<style scoped>
.calculator-button {
  position: relative;
  width: 100%;
  min-width: 45px;
  height: 45px;
  margin: 0;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.calculator-button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0,0,0,0.1);
}

.calculator-button:active {
  transform: scale(0.96);
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

/* Ripple effect */
.ripple {
  position: absolute;
  border-radius: 50%;
  transform: scale(0);
  animation: ripple 0.6s linear;
  background-color: rgba(255, 255, 255, 0.7);
}

@keyframes ripple {
  to {
    transform: scale(4);
    opacity: 0;
  }
}

/* Digit buttons */
.calculator-button.digit {
  background-color: #f8f9fa;
  color: #333;
  font-weight: 500;
}

.calculator-button.digit:hover {
  background-color: #e9ecef;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Operator buttons */
.calculator-button.operator {
  background-color: #ffa726;
  color: white;
  font-weight: bold;
}

.calculator-button.operator:hover,
.calculator-button.operator.active {
  background-color: #fb8c00;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}

/* Function buttons (clear, equals) */
.calculator-button.function {
  background-color: #e57373;
  color: white;
  font-weight: 500;
}

.calculator-button.function:hover {
  background-color: #ef5350;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}

/* Memory buttons */
.calculator-button.memory {
  background-color: #90caf9;
  color: white;
  font-weight: 500;
}

.calculator-button.memory:hover {
  background-color: #64b5f6;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}

/* FIN button */
.calculator-button.fin {
  background-color: #81c784;
  color: white;
  font-weight: 500;
}

.calculator-button.fin:hover {
  background-color: #66bb6a;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}

/* Active state overlay */
.calculator-button.active::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
</style>