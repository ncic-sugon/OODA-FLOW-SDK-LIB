# OODA-FLOW-SDK-LIB
OODA workflow sdk library

The goal of this project is to build and apply open source platforms for deep learning applications.

Develop algorithm library and sample library for artificial intelligence application software, integrate two kinds of applications (biological image big data analysis, genetic data analysis), and demonstrate on sugon advanced computing platform.

Complete the function development of algorithm library and sample library. The machine learning algorithm is developed to accelerate the core library, which is deployed and integrated into sugon advanced computing service platform. Based on the home-made hugon processor, the library is available for users to call. The accelerated core library will be closely coupled to the optimization of high-performance computer system at all levels.

Implement the algorithm tool set that supports the efficient parallel execution of large-scale machine learning and partially open source. The algorithm tool set should be integrated into sugon advanced computing platform to provide application services.

Responsible for the transplantation and integration of more than two kinds of applications (big data analysis of biological image and gene data analysis) into sugon advanced computing service platform, completing the support of typical application process, and reaching the leading level in terms of performance and scalability.

GSWITCH is a pattern-based algorithmic autotuning system that dynamically switched to the suitable optimization variants with negligible overhead. Specifically, It is a CUDA library targeting the GPU-based graph processing application, it supports both vertex-centric or edge-centric abstractions. By far, GSWITCH can automatically determine the suitable optimization variants in Direction (push, pull), data-structure (Bitmap, Sorted Queue, Unsorted Queue), Load-Balance (TWC, WM, CM, STRICT, 2D-partition), Stepping (Increase, Decrease, Remain), Kernel Fusion(Standalone, Fused). The fast optimization transition of GSWITCH is based on a machine learning model trained from 600+ real graphs from the network repository. The model can be reused by news applications, or be retrained to adapt new architectures. In addition, GSWITCH provides succinct programming interface which hides all low-level tuning details. Developers can implements their graph application with high performance in just ~100 lines of code.
