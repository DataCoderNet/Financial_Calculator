<!-- Keep template and script sections exactly as they were, only updating the menu positioning styles -->
<style scoped>
.fin-menu {
  position: relative;
  display: inline-block;
  z-index: 100;
}

.menu-content {
  position: absolute;
  top: 0;
  left: 0;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  min-width: 280px;
  max-height: 80vh;
  overflow-y: auto;
  padding: 0;
  backdrop-filter: blur(10px);
}

.main-menu {
  overflow: hidden;
}

.menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  border-radius: 12px 12px 0 0;
}

.menu-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6c757d;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.close-button:hover {
  color: #2c3e50;
  background-color: rgba(0, 0, 0, 0.05);
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  padding: 16px;
}

/* Transitions */
.menu-enter-active,
.menu-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.category-enter-active,
.category-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.category-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.category-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Scrollbar styling */
.menu-content::-webkit-scrollbar {
  width: 8px;
}

.menu-content::-webkit-scrollbar-track {
  background: #f8f9fa;
  border-radius: 4px;
}

.menu-content::-webkit-scrollbar-thumb {
  background-color: #ced4da;
  border-radius: 4px;
}

.menu-content::-webkit-scrollbar-thumb:hover {
  background-color: #adb5bd;
}
</style>