<template>
  <div class="tvm-menu-container">
    <button class="fin-button" @click="toggleMenu">FIN</button>
    <div v-if="isOpen" class="tvm-menu">
      <div class="tvm-header">
        <h3>Time Value of Money</h3>
        <button @click="toggleMenu" class="close-button">&times;</button>
      </div>
      <div class="parameter-buttons">
        <button 
          v-for="param in parameterButtons" 
          :key="param.key"
          class="param-button"
          :class="{ 'calculated': lastCalculated === param.key }"
          @click="handleParameterClick(param)"
        >
          {{ param.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TVMMenu',
  data() {
    return {
      isOpen: false,
      parameters: {
        n: null,
        i: null,
        pv: null,
        pmt: null,
        fv: null,
        pyr: 12,
        end: true
      },
      lastCalculated: '',
      parameterButtons: [
        { key: 'n', label: 'N' },
        { key: 'i', label: 'I%YR' },
        { key: 'pv', label: 'PV' },
        { key: 'pmt', label: 'PMT' },
        { key: 'fv', label: 'FV' }
      ]
    }
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen
      this.$emit('menu-state', this.isOpen)
    },
    handleParameterClick(param) {
      this.$emit('assign-value', param)
    },
    assignParameterValue(key, value) {
      this.parameters[key] = parseFloat(value)
      this.$emit('parameter-update', this.parameters)
      
      // Check if we can calculate a missing parameter
      const unsetParams = this.parameterButtons
        .filter(p => this.parameters[p.key] === null)
      
      if (unsetParams.length === 1) {
        const missingParam = unsetParams[0]
        this.calculateParameter(missingParam.key)
      }
    },
    async calculateParameter(paramToCalculate) {
      try {
        const response = await fetch('/api/fin/tvm/' + paramToCalculate, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            n: this.parameters.n,
            i: this.parameters.i,
            pv: this.parameters.pv,
            pmt: this.parameters.pmt,
            fv: this.parameters.fv,
            pyr: this.parameters.pyr,
            end: this.parameters.end
          })
        })
        
        const result = await response.json()
        if (response.ok) {
          this.parameters[paramToCalculate] = result.value
          this.lastCalculated = paramToCalculate
          this.$emit('parameter-update', this.parameters)
          this.$emit('calculation-request', {
            parameter: paramToCalculate,
            value: result.value
          })
        } else {
          console.error('Calculation error:', result.message)
        }
      } catch (error) {
        console.error('Network error:', error)
      }
    },
    resetState() {
      this.parameters = {
        n: null,
        i: null,
        pv: null,
        pmt: null,
        fv: null,
        pyr: 12,
        end: true
      }
      this.lastCalculated = ''
      this.isOpen = false
      this.$emit('parameter-update', this.parameters)
    }
  }
}
</script>

<style scoped>
.tvm-menu-container {
  position: relative;
}

.fin-button {
  padding: 10px 20px;
  font-size: 1rem;
  color: #fff;
  background-color: #2196f3;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.fin-button:hover {
  background-color: #1976d2;
}

.tvm-menu {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  width: 380px; /* Match calculator width */
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  z-index: 1000;
}

.tvm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.tvm-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0 5px;
}

.close-button:hover {
  color: #333;
}

.parameter-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  padding: 15px;
}

.param-button {
  padding: 12px;
  font-size: 1rem;
  color: #333;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.param-button:hover {
  background-color: #e3f2fd;
  border-color: #2196f3;
  color: #1976d2;
}

.param-button.calculated {
  background-color: #e8f5e9;
  border-color: #4caf50;
  color: #2e7d32;
}
</style>