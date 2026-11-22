#stdint.h or basic types definition for freestanding environment
typedef unsigned char uint8_t;
typedef unsigned short uint16_t;

void kernel_main(void) {
    // VGA text mode buffer address
    volatile uint16_t* vga_buffer = (volatile uint16_t*) 0xB8000;
    const char* message = "Hello from Custom OS Kernel!";
    
    int index = 0;
    while (message[index] != '\0') {
        // Character + white text on black background attribute (0x0F)
        vga_buffer[index] = (uint16_t)message[index] | (0x0F << 8);
        index++;
    }
    
    // Halt the CPU
    while (1) {
        __asm__ __volatile__("hlt");
    }
}
