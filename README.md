# S3 Dataset (S3D)
S3 Dataset (S3D) with Generation Code and Resources
## Contents
1. **Datasets**
  1. MedlinePlus
    1. **MedlinePlus-SemRep.xls**
      * A two-column table (in .xls format) that presents the annotated version of each sentence in the MedlinePlus dataset along with the proposed simplification.
    2. **MedlinePlus-SemRep.xml**
      * For each sentence in the MedlinePlus dataset, we provide:
        1. Its annotated version
        2. Its simplification
        3. The triples-facts that have been identified in the original sentence
  2. WikiAstronauts
    1. **WikiAstronauts-DBpedia.xls**
      * A two-column table (in .xls format) that presents the annotated version of each sentence in the WikiAstronauts dataset along with the proposed simplification.
    2. **WikiAstronauts-DBpedia.xml**
      * For each sentence in the WikiAstronauts dataset, we provide:
        1. Its annotated version
        2. Its simplification
        3. The triples-facts that have been identified in the original sentence
2. Evaluations
  1. MedlinePlus-SemRep.xls
  2. WikiAstronauts-DBpedia.xls
    * The tables (in .xls format) that have been used to evaluate the methods according to which a simplification is selected.
3. src
  1. CrowdFlower
    1. MedlinePlus
      1. experiment.csv 
        * The table (in .csv format) that was used on the CrowdFlower platform. 
        * It contains the annotated version of the sentences from the MedlinePlus dataset.
      2. f902529.csv
        * The table (in .csv format) that contains all the simplifications that have been submitted by the contributors.
    2. WikiAstronauts
      1. experiment.csv 
        * The table (in .csv format) that was used on the CrowdFlower platform.
        * It contains the annotated version of the sentences from the WikiAstronauts dataset.
      2. f900315.csv
        * The table (in .csv format) that contains all the simplifications that have been submitted by the contributors.
  2. Data
    1. MedlinePlus
    2. WikiAstronauts
      * Folders that contain (in .csv and .xml format) the original sentences from the two datasets along with their respective annotated versions and the triples-facts.
  3. ```Dataset-MedlinePlus.py```
    * Python script that parses the original sentences that are found at ```./Data/MedlinePlus/XML```.
    * Provides various statistics regarding the dataset.
    * Stores the CrowdFlower table (in .csv format) at ```./CrowdFlower/MedlinePlus/experiment.csv```.
  4. ```Dataset-WikiAstronauts.py```
    * Python script that parses the original sentences that are found at ```./Data/WikiAstronauts/XML```.
    * Provides various statistics regarding the dataset.
    * Stores the CrowdFlower table (in .csv format) at ```./CrowdFlower/WikiAstronauts/experiment.csv```.
  5. ```Output-MedlinePlus.py```
    * Python script that processes the simplifications that are proposed by the contributors and are located at ```./CrowdFlower/MedlinePlus/f902529.csv```.
    * Implements a variety of metrics in order to choose the most appropriate simplification.
    * By commenting-in the evaluation section of the code, it is able to select 30 random sentences that are used for the evaluation purposes and are stored by default at ```../Evaluation/MedlinePlus-SemRep.xls```.
  6. ```Output-WikiAstronauts.py```
    * Python script that processes the simplifications that are proposed by the contributors and are located at ```./CrowdFlower/WikiAstronauts/f900315.csv```.
    * Implements a variety of metrics in order to choose the most appropriate simplification.
    * By commenting-in the evaluation section of the code, it is able to select 30 random sentences that are used for the evaluation purposes and are stored by default at ```../Evaluation/WikiAstronauts-DBpedia.xls```.

## License
This project is licensed under the terms of the Apache 2.0 License.
