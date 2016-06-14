# KB-Text-Alignment
Aligning Texts and Knowledge Bases with Semantic Sentence Simplification
## Folders
1. Datasets
  1. MedlinePlus
    1. MedlinePlus-SemRep.xls
      * A two-column table (in .xls format) that presents the annotated version of each sentence in the MedlinePlus dataset along with the proposed simplification.
    2. MedlinePlus-SemRep.xml
      * For each sentence in the MedlinePlus dataset, we provide:
        1. Its annotated version
        2. Its simplification
        3. The triples-facts that have been identified in the original sentence
  2. WikiAstronauts
    1. WikiAstronauts-DBpedia.xls
      * A two-column table (in .xls format) that presents the annotated version of each sentence in the WikiAstronauts dataset along with the proposed simplification.
    2. WikiAstronauts-DBpedia.xml
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
      * Folders that contain (in .csv and .xml format) the original sentences from the two datasets along with their respective annotatated versions and the triples-facts.

## License
This project is licensed under the terms of the Apache 2.0 License.
