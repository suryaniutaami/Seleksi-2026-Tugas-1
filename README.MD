# Seleksi-2026-Tugas-1
Program ini merupakan implementasi proses web scraping dan pembangunan database `exercise` sebagai bagian dari Tugas Seleksi 1 Asisten mata kuliah IF2240 Basis Data.

## Daftar Isi

- [Deskripsi Singkat](#deskripsi-singkat)
- [Author](#author)
- [Struktur Proyek](#struktur-proyek)
- [Requirements](#requirements)
- [Cara Penggunaan](#cara-penggunaan)
  - [Scraping](#scraping)
  - [Transform](#transform)
  - [Seeding](#seeding)
  - [Inisialisasi Database](#inisialisasi-database)
- [Struktur ERD dan Diagram Relasional](#struktur-erd-dan-diagram-relasional)
- [Automated Scheduling](#automated-scheduling)
  - [Membuat User Pipeline](#membuat-user-pipeline)
  - [Konfigurasi Database Lokal](#konfigurasi-database-lokal)
  - [Otomasi Proses](#otomasi-proses)
  - [Pencegahan Redundansi](#pencegahan-redundansi)
  - [Waktu Pelaksanaan](#waktu-pelaksanaan)
- [Screenshot Database](#screenshot-database)
- [Referensi](#referensi)

## Deskripsi Singkat
Data yang dikumpulkan dan diimplementasikan ke dalam DBMS merupakan data exercise yang diperoleh dari [MuscleWiki](https://musclewiki.com/). Secara keseluruhan, database ini menyimpan informasi mengenai workout, target area, kategori, langkah panduan, serta program workout.

Workout menjadi salah satu aktivitas olahraga yang banyak diminati. Namun, banyaknya jenis gerakan dan variasi workout dapat menyulitkan pengguna dalam mencari latihan yang sesuai, terutama bagi pemula yang ingin menyusun resep program berdasarkan kebutuhan dan kemampuan masing-masing.

[MuscleWiki](https://musclewiki.com/) dipilih sebagai sumber data karena menyediakan informasi workout yang cukup lengkap. Meskipun demikian, proses pencarian pada website tersebut masih memiliki keterbatasan. Misalnya, pengguna hanya dapat melihat daftar workout berdasarkan satu target area dan satu filter dalam satu waktu. 

Melalui database `exercise`, data dari berbagai target dan kategori dapat dikombinasikan secara lebih fleksibel menggunakan query. Pengguna dapat mencari workout berdasarkan beberapa target area sekaligus maupun berdasarkan atribut lain, seperti kategori, tingkat kesulitan, mekanisme gerakan, force, grip, dan tag. Sehingga, database ini diharapkan dapat mempermudah pengguna, terutama pemula, dalam mencari workout dan menyusun program latihan yang sesuai dengan kebutuhan.

## Author
| NIM | Nama |
|:---:|:---:|
| 13524042 | Suryani Mulia Utami

## Struktur Proyek

```text
Seleksi-2026-Tugas-1/
│
├── Data Scraping/
│   ├── src/
│   │   ├── scraper/
│   │   │   ├── main.py
│   │   │   ├── scrape_filters.py
│   │   │   ├── scrape_target_areas.py
│   │   │   ├── scrape_listings.py
│   │   │   ├── scrape_workouts.py
│   │   │   └── scrape_programs.py
│   │   │
│   │   ├── transform/
│   │   │   ├── main.py
│   │   │   ├── build_relations.py
│   │   │   ├── deduplicate.py
│   │   │   ├── normalize.py
│   │   │   └── parse.py
│   │   │
│   │   └── helpers/
│   │
│   └── data/
│       ├── raw/
│       │   ├── history/20260723_112820/  # history batch 1
│       │   ├── history/20260723_112820/  # history batch 2
│       │   │
│       │   ├── filters.json
│       │   ├── target_areas.json
│       │   ├── listings.json
│       │   ├── workouts.json
│       │   └── programs.json
│       │
│       └── processed/
│           ├── categories.json
│           ├── target_areas.json
│           ├── workouts.json
│           ├── workout_grips.json
│           ├── steps.json
│           ├── workout_tags.json
│           ├── workout_targets.json
│           ├── programs.json
│           └── program_workouts.json
│   
├── Data Storing/
│   ├── src/
│   │   ├── schema/
│   │   ├── constraints/
│   │   ├── helpers/
│   │   ├── seed/
│   │   │   └── seed.sql
│   │   ├── seeder/
│   │   └── exercise.sql  # jalankan sekali di awal untuk initiate database
│   │
│   ├── design/
│   │   ├── erd_exercise.png
│   │   └── relational_diagram_exercise.png
│   │
│   ├── export/
│   │   ├── exercise_dump_20260723_112820.sql   # dump batch 1
│   │   └── exercise_dump_20260723_112820.sql   # dump batch 2
│   │
│   └── screenshot/
│
├── config/
│   └── pipeline.cnf.example
│
├── Query Optimasi/
│   ├── screenshot/
│   └── query_optimasi.sql
│
├── scheduled_pipeline.bat  # automated scheduling
├── requirements.txt
└── README.md
```

## Requirements
* `Playwright`, `Playwright Chromium`, dan `Tzdata` 
```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Cara Penggunaan
Pipeline pengolahan data terdiri atas:

Scraping -> Transform -> Seeding -> Database

### Scraping 

```bash
cd "Data Scraping"
python -m src.scraper.main
```

#### Output

Output proses scraping disimpan pada: `Data Scraping/data/raw/`

File yang dihasilkan:
- `filters.json`
- `target_areas.json`
- `listings.json`
- `workouts.json`
- `programs.json`

Struktur `filters.json`:
```bash
{
  "name": "...",
  "scrape_metadata": {
    "dom_index": 0,
    "filter_id": "...",
    "selector": "...",
    "scraped_at": "..."
  }
}
```

Struktur `target_areas.json`:
```bash
{
  "name": "...",
  "class": "...",
  "scrape_metadata": {
    "dom_index": 0,
    "selector": "...",
    "scraped_at": "..."
  }
}
```

Struktur `listings.json`:
```bash
{
  "target_name": "...",
  "filter_name": "...",
  "page_number": 1,
  "workout_count": 0,
  "workouts": [
    {
      "name": "...",
      "detail_url": "...",
      "scrape_metadata": {
        "dom_index": 0,
        "selector": "..."
      }
    }
  ],
  "scrape_metadata": {
    "url": "...",
    "page_url": "...",
    "scraped_at": "..."
  }
}
```

Struktur `workouts.json`:
```bash
{
  "target_name": "...",
  "filter_name": "...",
  "page_number": 1,
  "workout_count": 0,
  "workouts": [
    {
      "name": "...",
      "detail_url": "...",
      "scrape_metadata": {
        "dom_index": 0,
        "selector": "..."
      }
    }
  ],
  "scrape_metadata": {
    "url": "...",
    "page_url": "...",
    "scraped_at": "..."
  }
}
```
Struktur `programs.json`:
```bash
{
  "name": "...",
  "detail_url": "...",
  "difficulty": "...",
  "goal": "...",
  "description": "...",
  "workout_count": 0,
  "workout": [
    {
      "name": "...",
      "series": "...",
      "scrape_metadata": {
        "dom_index": 0,
        "selector_workout": "...",
        "selector_series": "..."
      }
    }
  ],
  "scrape_metadata": {
    "page_number": 1,
    "dom_index": 0,
    "selector": "...",
    "scraped_at": "..."
  }
}
```

### Transform
Masih di direktori `Data Scraping/`

Untuk membersihkan dan mempersiapkan data, jalankan:
```bash
python -m src.transform.main
```
#### Output
Output proses transform disimpan pada: `Data Scraping/data/processed/`

File yang dihasilkan:
- categories.json
- target_areas.json
- workouts.json
- workout_grips.json
- steps.json
- workout_tags.json
- workout_targets.json
- programs.json
- program_workouts.json

Berikut beberapa hal yang dilakukan pada tahap ini:
#### Parsing data
Parsing dilakukan untuk memecah nilai mentah yang masih tersimpan dalam satu string menjadi beberapa nilai terpisah.

Pada atribut grips, setiap grip yang awalnya dipisahkan dengan tanda koma diubah menjadi daftar grip individual. Setiap grip kemudian digunakan untuk membentuk data pada tabel WorkoutGrip.

Contoh:
```bash
"grips": "Overhand, Neutral, Underhand"
```
diubah menjadi:
```bash
"Overhand"
"Neutral"
"Underhand"
```
#### Normalisasi 

Normalisasi atribut CSS class yang diperoleh saat scraping ke dalam atribut tipe target dan role target.

Contoh:
```bash
# Tipe target
"class": "bodymap text-mw-gray ..."
"class": "joints text-mw-red ..." 
# Role target
"class": "bodymap text-muscle-primary"
```
diubah menjadi:

```bash
# Tipe target
"type": "Muscle"
"type": "Joint"
# Role target
"role": "Primary"
```
#### Deduplikasi 
Setelah data relasional dibentuk, setiap hasil diperiksa berdasarkan kombinasi key tertentu untuk memastikan setiap record unik.

### Seeding
```bash
cd /"Data Storing"
python -m src.seeder.main
```
#### Output
Output proses seeding disimpan pada: `Data Storing/src/seed/seed.sql`

### Inisialisasi Database
Jalankan file `exercise.sql` menggunakan MariaDB
```bash
mariadb -u root -p < "src\exercise.sql"
```
File exercise.sql akan menjalankan:
- Pembuatan database
- Pembuatan schema
- Apply constraints dan trigger
- Seeding data

## Struktur ERD dan Diagram Relasional 
  ### ERD:
  ![ERD](Data%20Storing/design/erd_exercise.png)

  ### Relational Diagram:
  ![Relational Diagram](Data%20Storing/design/relational_diagram_exercise.png)

  Proses translasi ERD mengikuti beberapa aturan sebagai berikut:
  1. Setiap entity (`program`, `workout`, `category`, `step`, `target_area`) pada ERD dibuat menjadi relasi.
  2. Relasi `terdiri` yang menghubungkan program-workout bersifat many-to-many, sehingga dibuat relasi `program_workout` yang atributnya adalah PK pada relasi program, PK pada relasi workout, dan *relation's attribute* yang terdapat pada ERD (duration dan order_number).
  3. Relasi `menargetkan` yang menghubungkan workout-target_area bersifat many-to-many, sehingga dibuat relasi `workout_target` yang atributnya adalah PK pada relasi workout, PK pada relasi target_area, dan *relation's attribute* yang terdapat pada ERD (role).
  4. Relasi `memiliki` menghubungkan workout-step di mana step adalah *Weak Entity*, sehingga PK dari workout dititipkan pada relasi `step`. Dengan begitu, PK dari relasi `step` adalah PK pada workout bersama dengan discriminator pada step (workout_name, step_number).
  5. Relasi `termasuk` yang menghubungkan workout->category bersifat many-to-one, sehingga PK dari entity category dititipkan pada relasi workout (*many side*). Oleh karena itu, *category_name* menjadi atribut dari relasi workout.
  6. Entity workout memiliki dua *multivalued attribute*, yaitu grip dan tag. Oleh karena itu, dibuat 2 relasi `workout_grip` dan `workout_tag` yang masing-masing memiliki PK dari workout sebagai atributnya. Dengan begitu, PK dari relasi `workout_grip` adalah (workout_name, grip) dan PK dari relasi `workout_tag` adalah (workout_name, tag)
  

## Automated Scheduling
Setelah menginisialisasi database, data dari database dapat di-update secara berkala. 

Proses scraping, transformasi, seeding, dan update data ke database akan dilakukan secara otomatis

### Cara Penggunaan

#### Membuat User Pipeline
Masuk ke MariaDB sebagai root:

```bash
mariadb -u root -p
```

kemudian jalankan:

```sql
CREATE USER IF NOT EXISTS 'pipeline_user'@'localhost'
IDENTIFIED BY 'PASSWORD_KAMU';

GRANT SELECT, INSERT, UPDATE, DELETE
ON exercise.*
TO 'pipeline_user'@'localhost';

FLUSH PRIVILEGES;
```

Pastikan password sama dengan password pada file config.

#### Konfigurasi Database Lokal
Salin template:

```text
config/pipeline.cnf.example
```

lalu simpan sebagai:

```text
%USERPROFILE%\.mariadb\pipeline.cnf
```

#### Otomasi proses
Coba jalankan `scheduled_pipeline.bat`. Bila berhasil, maka dapat dapat daftarkan `scheduled_pipeline.bat` pada *Windows Task Scheduler* agar proses dapat dijalankan secara berkala.

### Pencegahan Redundansi
Redundansi data dicegah dengan:
- SQL seeder menggunakan `ON DUPLICATE KEY UPDATE` atau `INSERT IGNORE` sehingga record dengan PK yang sama tidak akan ditambahkan sebagai record baru.

### Waktu Pelaksanaan 
Automated scheduling diuji dalam dua batch pada tanggal 23 Juli 2026 untuk menunjukkan bahwa pipeline dapat melakukan pembaruan data secara berkala.

Batch pertama dijalankan pada pukul **11:28:20 WIB**. Hasilnya disimpan pada:

```text
# Hasil data mentah
Data Scraping/data/raw/history/20260723_112820/

# Hasil dump
Data Storing/export/exercise_dump_20260723_112820.sql
```

Batch kedua dijalankan pada pukul **17:39:06 WIB**. Hasilnya disimpan pada:
```text
# Hasil data mentah
Data Scraping/data/raw/history/20260723_173906/

# Hasil dump
Data Storing/export/exercise_dump_20260723_173906.sql
```

## Screenshot Database
![show_tables](Data%20Storing/screenshot/show_tables.png)
![category](Data%20Storing/screenshot/category.png)
![target_area](Data%20Storing/screenshot/target_area.png)
![workout](Data%20Storing/screenshot/workout.png)
![workout_target](Data%20Storing/screenshot/workout_target.png)
![step](Data%20Storing/screenshot/step.png)
![workout_tag](Data%20Storing/screenshot/workout_tag.png)
![workout_grip](Data%20Storing/screenshot/workout_grip.png)
![program](Data%20Storing/screenshot/program.png)
![program_workout](Data%20Storing/screenshot/program_workout.png)


## Referensi

### Sumber Data
- [MuscleWiki](https://musclewiki.com/)

### Teknologi dan Library
- [Python](https://www.python.org/)
- [Playwright for Python](https://playwright.dev/python/)
- [MariaDB](https://mariadb.org/)
- [tzdata](https://pypi.org/project/tzdata/)
