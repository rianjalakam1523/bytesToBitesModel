#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>

// AUTHOR: RIAN JALAKAM, FALL 2026

#define THERMAL_PATH "/sys/class/thermal/thermal_zone0/temp"
#define MEMINFO_PATH "/proc/meminfo"

int get_hwmon_path(const char *target_name, char *path_out, size_t max_len) {
    DIR *dir = opendir("/sys/class/hwmon");
    if (!dir) return -1;

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_name[0] == '.') continue;

        char name_path[1024];
        snprintf(name_path, sizeof(name_path), "/sys/class/hwmon/%s/name", entry->d_name);
        
        FILE *f = fopen(name_path, "r");
        if (f) {
            char dev_name[64];
            if (fgets(dev_name, sizeof(dev_name), f)) {
                dev_name[strcspn(dev_name, "\r\n")] = 0;
                if (strcmp(dev_name, target_name) == 0) {
                    snprintf(path_out, max_len, "/sys/class/hwmon/%s", entry->d_name);
                    fclose(f);
                    closedir(dir);
                    return 0;
                }
            }
            fclose(f);
        }
    }
    closedir(dir);
    return -1;
}

void check_system_stats() {
    // 1. Read CPU Temperature
    FILE *f_temp = fopen(THERMAL_PATH, "r");
    if (f_temp) {
        int temp_milli;
        if (fscanf(f_temp, "%d", &temp_milli) == 1) {
            printf("[Jetson Telemetry] CPU Temperature: %.2f°C\n", temp_milli / 1000.0);
        }
        fclose(f_temp);
    }

    // 2. Read Voltage from INA3221 (hwmon3) with a larger destination buffer
    char hwmon_dir[1024];
    if (get_hwmon_path("ina3221", hwmon_dir, sizeof(hwmon_dir)) == 0) {
        char volt_path[2048]; // Expanded to prevent format-truncation warning
        snprintf(volt_path, sizeof(volt_path), "%s/in1_input", hwmon_dir);
        
        FILE *f_volt = fopen(volt_path, "r");
        if (f_volt) {
            int volt_milli;
            if (fscanf(f_volt, "%d", &volt_milli) == 1) {
                printf("[Jetson Telemetry] Rail Voltage (VDD_IN): %.3f V\n", volt_milli / 1000.0);
            }
            fclose(f_volt);
        }
    } else {
        printf("[Jetson Telemetry] Voltage sensor path not active (check hwmon index).\n");
    }

    // 3. Read RAM Usage
    FILE *f_mem = fopen(MEMINFO_PATH, "r");
    if (f_mem) {
        char line[256];
        long mem_free = -1, mem_total = -1;
        while (fgets(line, sizeof(line), f_mem)) {
            if (strncmp(line, "MemTotal:", 9) == 0) {
                sscanf(line, "MemTotal: %ld kB", &mem_total);
            } else if (strncmp(line, "MemAvailable:", 13) == 0) {
                sscanf(line, "MemAvailable: %ld kB", &mem_free);
            }
        }
        fclose(f_mem);
        if (mem_total > 0 && mem_free > 0) {
            printf("[Jetson Telemetry] RAM Used: %ld MB / %ld MB (Available: %ld MB)\n", 
                   (mem_total - mem_free) / 1024, mem_total / 1024, mem_free / 1024);
        }
    }
}

int main() {
    setbuf(stdout, NULL);
    printf("Starting Monitor...\n");
    while (1) {
        check_system_stats();
        printf("--------------------------------------------------\n");
        sleep(3);
    }
    return 0;
}
