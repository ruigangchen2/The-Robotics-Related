import numpy as np
import matplotlib.pyplot as plt
import pandas

#no clutch the first group
angle = np.array([32.56, 32.55, 32.51, 32.50, 32.52, 32.55, 32.55, 32.56, 32.49, 32.31, 32.16, 31.68, 31.37, 30.88, 30.63, 30.59, 30.66, 30.71, 30.33, 29.58, 28.84, 28.51, 27.96, 27.77, 27.04, 26.06, 25.67, 25.00, 24.40, 24.11, 23.53, 22.75, 21.37, 20.34, 19.90, 19.21, 18.74, 18.54, 17.06, 15.79, 15.23, 14.27, 13.86, 13.18, 11.65, 11.02, 9.92, 9.08, 8.72, 8.06, 6.99, 6.29, 5.03, 3.95, 3.48, 2.68, 2.36, 1.36, 0.23, -0.29, -1.24, -2.07, -2.46, -3.42, -4.47, -4.93, -5.72, -6.08, -6.76, -7.41, -7.84, -8.64, -9.37, -9.70, -10.32, -10.88, -11.14, -11.68, -11.93, -12.46, -12.99, -13.25, -13.75, -13.98, -14.10, -14.38, -14.68, -14.86, -15.26, -15.48, -15.47, -15.55, -15.61, -15.79, -16.03, -16.17, -15.94, -15.84, -15.84, -15.93, -16.00, -16.18, -15.98, -15.71, -15.29, -15.02, -14.94, -14.86, -14.42, -14.03, -13.40, -12.88, -12.67, -12.32, -12.19, -11.48, -10.45, -10.02, -9.29, -8.69, -8.41, -7.94, -6.62, -6.04, -5.03, -4.61, -3.87, -3.29, -2.63, -1.43, -0.38, 0.10, 0.95, 1.33, 2.00, 3.16, 3.69, 4.63, 5.49, 5.90, 6.65, 7.71, 8.20, 9.10, 9.49, 10.25, 10.94, 11.28, 11.99, 12.69, 13.01, 13.66, 14.25, 14.54, 15.00, 15.18, 15.55, 15.97, 16.19, 16.63, 16.82, 16.79, 16.82, 16.84, 16.94, 17.13, 17.25, 17.22, 16.94, 16.85, 16.77, 16.76, 16.78, 16.44, 16.11, 15.57, 15.20, 15.05, 14.84, 14.75, 14.29, 13.51, 13.16, 12.59, 12.18, 12.01, 11.73, 10.72, 10.27, 9.51, 8.90, 8.62, 8.17, 7.59, 6.58, 5.73, 5.34, 4.69, 4.14, 3.89, 2.80, 1.85, 1.43, 0.70, 0.38, -0.23, -1.17, -1.58, -2.34, -2.98, -3.26, -3.78, -4.36, -4.69, -5.30, -5.58, -6.11, -6.61, -6.84, -7.31, -7.78, -8.01, -8.45, -8.68, -9.12, -9.53, -9.72, -10.10, -10.50, -10.69, -11.10, -11.52, -11.59, -11.75, -11.85, -12.07, -12.34, -12.48, -12.56, -12.48, -12.46, -12.50, -12.60, -12.67, -12.86, -12.68, -12.36, -12.16, -12.10, -11.99, -11.99, -12.02, -12.10, -12.23, -12.31, -12.49, -12.59, -12.83, -11.69, -11.20, -10.37, -9.68, -9.40, -8.94, -8.20, -7.71, -6.81, -6.06, -5.72, -5.11, -4.83, -3.72, -2.77, -2.34, -1.61, -0.98, -0.69, 0.08, 0.56, 1.43, 2.17, 2.50, 3.12, 3.85, 4.26, 5.06, 5.42, 6.12, 6.75, 7.04, 7.65, 8.30, 8.60, 9.18, 9.72, 9.99, 10.50, 10.72, 11.18, 11.59, 11.81, 12.23, 12.64, 12.67, 12.77, 12.84, 13.02, 13.21, 13.32, 13.56, 13.37, 13.31, 13.24, 13.26, 13.28, 13.37, 13.18, 12.87, 12.65, 12.57, 12.48, 12.44, 12.46, 11.90, 11.66, 11.27, 10.97, 10.86, 10.69, 10.22, 9.87, 9.27, 8.78, 8.58, 8.25, 8.10, 7.27, 6.59, 6.29, 5.77, 5.35, 5.16, 4.59, 4.22, 3.54, 2.98, 2.72, 2.27, 1.65, 1.27, 0.59, 0.01, -0.25, -0.72, -0.94, -1.45, -2.07, -2.35, -2.86, -3.30, -3.51, -3.94, -4.42, -4.64, -5.05, -5.24, -5.63, -6.03, -6.22, -6.59, -6.95, -7.13, -7.48, -7.81, -7.98, -8.17, -8.27, -8.49, -8.71, -8.83, -9.09, -9.11, -9.15, -9.23, -9.34, -9.42, -9.59, -9.67, -9.48, -9.36, -9.34, -9.30, -9.32, -9.34, -9.15, -8.84, -8.71, -8.50, -8.42, -8.30, -7.99, -7.75, -7.35, -7.03, -6.89, -6.70, -6.54, -6.26, -5.77, -5.57, -5.22, -4.94, -4.84, -4.36, -3.68, -3.38, -2.84, -2.39, -2.17, -1.82, -1.43, -0.77, -0.17, 0.10, 0.59, 1.01, 1.19, 1.79, 2.05, 2.51, 2.95, 3.15, 3.51, 4.04, 4.29, 4.76, 5.19, 5.40, 5.77, 5.94, 6.36, 6.77, 6.98, 7.38, 7.74, 7.92, 8.20, 8.33, 8.58, 8.86, 8.99, 9.27, 9.39, 9.38, 9.40, 9.43, 9.47, 9.56, 9.62, 9.43, 9.30, 9.26, 9.22, 9.22, 9.23, 9.07, 8.93, 8.70, 8.52, 8.47, 8.40, 8.39, 8.17, 7.81, 7.53, 7.42, 7.20, 7.13, 6.79, 6.29, 6.08, 5.72, 5.42, 5.29, 5.09, 4.81, 4.34, 3.94, 3.77, 3.47, 3.23, 2.95, 2.49, 2.06, 1.88, 1.54, 1.39, 1.13, 0.64, 0.43, 0.05, -0.30, -0.47, -0.77, -1.25, -1.45, -1.85, -2.04, -2.37, -2.69, -2.83, -3.14, -3.43, -3.57, -3.84, -3.97, -4.22, -4.43, -4.53, -4.73, -4.93, -5.04, -5.26, -5.41, -5.47, -5.58, -5.64, -5.78, -5.95, -6.02, -6.07, -6.05, -6.04, -6.06, -6.10, -6.16, -6.12, -6.06, -5.95, -5.91, -5.90, -5.89, -5.90, -5.76, -5.56, -5.41, -5.35, -5.27, -5.23, -5.17, -4.86, -4.73, -4.53, -4.36, -4.30, -4.19, -3.79, -3.62, -3.32, -3.19, -2.97, -2.79, -2.71, -2.24, -1.85, -1.67, -1.35, -1.21, -0.94, -0.53, -0.35, -0.01, 0.30, 0.46, 0.73, 1.07, 1.25, 1.57, 1.72, 2.00, 2.24, 2.35, 2.58, 2.78, 2.89, 3.09, 3.18, 3.37, 3.59, 3.73, 3.97, 4.19, 4.31, 4.53, 4.75, 4.85, 5.05, 5.14, 5.33, 5.52, 5.60, 5.67, 5.65, 5.65, 5.66, 5.67, 5.74, 5.78, 5.73, 5.63, 5.57, 5.56, 5.54, 5.54, 5.46, 5.32, 5.26, 5.17, 5.11, 5.08, 5.06, 4.87, 4.80, 4.68, 4.60, 4.58, 4.53, 4.51, 4.22, 4.00, 3.89, 3.71, 3.57, 3.50, 3.15, 3.00, 2.74, 2.51, 2.39, 2.22, 1.99, 1.87, 1.63, 1.42, 1.34, 1.17, 1.10, 0.85, 0.61, 0.51, 0.31, 0.11, 0.04, -0.17, -0.27, -0.48, -0.68, -0.76, -0.94, -1.11, -1.20, -1.38, -1.46, -1.63, -1.78, -1.84, -1.94, -1.99, -2.03, -2.09, -2.17, -2.21, -2.31, -2.32, -2.34, -2.40, -2.43, -2.48, -2.53, -2.52, -2.52, -2.52, -2.52, -2.53, -2.56, -2.61, -2.51, -2.47, -2.41, -2.36, -2.34, -2.32, -2.21, -2.03, -1.89, -1.84, -1.74, -1.68, -1.66, -1.52, -1.38, -1.33, -1.24, -1.21, -1.16, -1.03, -0.94, -0.80, -0.66, -0.60, -0.52, -0.37, -0.29, -0.13, -0.06, 0.04, 0.16, 0.20, 0.33, 0.49, 0.58, 0.72, 0.85, 0.91, 1.05, 1.12, 1.26, 1.38, 1.43, 1.56, 1.65, 1.69, 1.76, 1.79, 1.88, 1.97, 2.02, 2.10, 2.19, 2.24, 2.32, 2.43, 2.48, 2.56, 2.55, 2.57, 2.58, 2.58, 2.61, 2.65, 2.68, 2.62, 2.60, 2.58, 2.58, 2.59, 2.60, 2.47, 2.41, 2.32, 2.25, 2.23, 2.19, 2.18, 2.08, 2.00, 1.97, 1.93, 1.88, 1.86, 1.72, 1.66, 1.56, 1.50, 1.45, 1.38, 1.27, 1.17, 1.00, 0.88, 0.83, 0.71, 0.66, 0.52, 0.34, 0.27, 0.12, 0.01, -0.04, -0.15, -0.19, -0.29, -0.37, -0.39, -0.47, -0.54, -0.61, -0.72, -0.79, -0.90, -0.99, -1.05, -1.15, -1.21, -1.24, -1.33, -1.41, -1.44, -1.52, -1.53, -1.53, -1.54, -1.56, -1.61, -1.64, -1.61, -1.56, -1.55, -1.55, -1.55, -1.55, -1.56, -1.48, -1.44, -1.39, -1.35, -1.33, -1.30, -1.29, -1.21, -1.16, -1.14, -1.11, -1.09, -1.08, -0.98, -0.94, -0.87, -0.82, -0.80, -0.75, -0.64, -0.57, -0.44, -0.35, -0.29, -0.20, -0.16, -0.06, 0.05, 0.10, 0.17, 0.23, 0.27, 0.35, 0.44, 0.49, 0.58, 0.61, 0.68, 0.75, 0.79, 0.88, 0.97, 1.00, 1.08, 1.13, 1.21, 1.30, 1.35, 1.45, 1.52, 1.56, 1.63, 1.65, 1.69, 1.72, 1.73, 1.80, 1.85, 1.83, 1.78, 1.76, 1.76, 1.76, 1.76, 1.77, 1.72, 1.69, 1.66, 1.63, 1.64, 1.66, 1.65, 1.61, 1.61, 1.61, 1.62, 1.63, 1.64, 1.56, 1.53, 1.44, 1.37, 1.34, 1.30, 1.17, 1.12, 1.03, 0.99, 0.93, 0.85, 0.82, 0.74, 0.68, 0.66, 0.61, 0.55, 0.53, 0.48, 0.44, 0.35, 0.28, 0.26, 0.20, 0.11, 0.06, -0.02, -0.07, -0.16, -0.23, -0.25, -0.33, -0.38, -0.40, -0.43, -0.50, -0.52, -0.56, -0.57, -0.58, -0.60, -0.62, -0.67, -0.71, -0.70, -0.68, -0.67, -0.66, -0.70, -0.71, -0.74, -0.76, -0.77, -0.79, -0.80, -0.82, -0.85, -0.84, -0.82, -0.81, -0.81, -0.81, -0.81, -0.81, -0.82, -0.82, -0.83, -0.85, -0.86, -0.89, -0.84, -0.80, -0.76, -0.76, -0.74, -0.72, -0.70, -0.64, -0.58, -0.53, -0.49, -0.46, -0.44, -0.44, -0.41, -0.36, -0.31, -0.27, -0.24, -0.18, -0.10, -0.03, 0.03, 0.03, 0.08, 0.13, 0.22, 0.29, 0.36, 0.42, 0.46, 0.55, 0.55, 0.62, ])
time = np.array([0, 11, 21, 31, 40, 51, 61, 71, 81, 90, 101, 111, 121, 130, 141, 151, 161, 170, 181, 191, 201, 211, 221, 231, 241, 251, 260, 271, 281, 291, 300, 311, 321, 331, 340, 351, 361, 371, 381, 391, 401, 411, 421, 430, 441, 451, 461, 470, 481, 491, 501, 510, 521, 531, 541, 551, 560, 571, 581, 591, 600, 611, 621, 631, 640, 651, 661, 671, 680, 691, 701, 711, 721, 730, 741, 751, 761, 770, 781, 791, 801, 810, 821, 831, 841, 851, 861, 871, 881, 891, 900, 911, 921, 931, 940, 951, 961, 971, 980, 991, 1001, 1011, 1021, 1031, 1041, 1051, 1061, 1070, 1081, 1091, 1101, 1110, 1121, 1131, 1141, 1150, 1161, 1171, 1181, 1191, 1200, 1211, 1221, 1231, 1240, 1251, 1261, 1271, 1280, 1291, 1301, 1311, 1320, 1331, 1341, 1351, 1361, 1370, 1381, 1391, 1401, 1410, 1421, 1431, 1441, 1450, 1461, 1471, 1481, 1491, 1501, 1511, 1521, 1531, 1540, 1551, 1561, 1571, 1580, 1591, 1601, 1611, 1620, 1631, 1641, 1651, 1661, 1671, 1681, 1691, 1701, 1710, 1721, 1731, 1741, 1750, 1761, 1771, 1781, 1790, 1801, 1811, 1821, 1831, 1840, 1851, 1861, 1871, 1880, 1891, 1901, 1911, 1920, 1931, 1941, 1951, 1960, 1971, 1981, 1991, 2001, 2010, 2021, 2031, 2041, 2050, 2061, 2071, 2081, 2090, 2101, 2111, 2121, 2131, 2141, 2151, 2161, 2171, 2180, 2191, 2201, 2211, 2220, 2231, 2241, 2251, 2260, 2271, 2281, 2291, 2301, 2311, 2321, 2331, 2341, 2350, 2361, 2371, 2381, 2390, 2401, 2411, 2421, 2430, 2441, 2451, 2461, 2471, 2480, 2491, 2501, 2511, 2520, 2531, 2541, 2551, 2560, 2571, 2581, 2591, 2600, 2611, 2621, 2631, 2641, 2650, 2661, 2671, 2681, 2690, 2701, 2711, 2721, 2730, 2741, 2751, 2761, 2771, 2781, 2791, 2801, 2811, 2820, 2831, 2841, 2851, 2860, 2871, 2881, 2891, 2900, 2911, 2921, 2931, 2941, 2951, 2961, 2971, 2981, 2990, 3001, 3011, 3021, 3030, 3041, 3051, 3061, 3070, 3081, 3091, 3101, 3111, 3120, 3131, 3141, 3151, 3160, 3171, 3181, 3191, 3200, 3211, 3221, 3231, 3240, 3251, 3261, 3271, 3281, 3290, 3301, 3311, 3321, 3330, 3341, 3351, 3361, 3370, 3381, 3391, 3401, 3411, 3421, 3431, 3441, 3451, 3460, 3471, 3481, 3491, 3500, 3511, 3521, 3531, 3540, 3551, 3561, 3571, 3581, 3591, 3601, 3611, 3621, 3630, 3641, 3651, 3661, 3670, 3681, 3691, 3701, 3710, 3721, 3731, 3741, 3751, 3760, 3771, 3781, 3791, 3800, 3811, 3821, 3831, 3840, 3851, 3861, 3871, 3880, 3891, 3901, 3911, 3921, 3930, 3941, 3951, 3961, 3970, 3981, 3991, 4001, 4010, 4021, 4031, 4041, 4051, 4061, 4071, 4081, 4091, 4100, 4111, 4121, 4131, 4140, 4151, 4161, 4171, 4180, 4191, 4201, 4211, 4221, 4231, 4241, 4251, 4261, 4270, 4281, 4291, 4301, 4310, 4321, 4331, 4341, 4350, 4361, 4371, 4381, 4391, 4400, 4411, 4421, 4431, 4440, 4451, 4461, 4471, 4480, 4491, 4501, 4511, 4520, 4531, 4541, 4551, 4561, 4570, 4581, 4591, 4601, 4610, 4621, 4631, 4641, 4650, 4661, 4671, 4681, 4691, 4701, 4711, 4721, 4731, 4740, 4751, 4761, 4771, 4780, 4791, 4801, 4811, 4820, 4831, 4841, 4851, 4861, 4871, 4881, 4891, 4901, 4910, 4921, 4931, 4941, 4950, 4961, 4971, 4981, 4990, 5001, 5011, 5021, 5031, 5040, 5051, 5061, 5071, 5080, 5091, 5101, 5111, 5120, 5131, 5141, 5151, 5160, 5171, 5181, 5191, 5201, 5210, 5221, 5231, 5241, 5250, 5261, 5271, 5281, 5290, 5301, 5311, 5321, 5331, 5341, 5351, 5361, 5371, 5380, 5391, 5401, 5411, 5420, 5431, 5441, 5451, 5460, 5471, 5481, 5491, 5501, 5511, 5521, 5531, 5541, 5550, 5561, 5571, 5581, 5590, 5601, 5611, 5621, 5630, 5641, 5651, 5661, 5671, 5680, 5691, 5701, 5711, 5720, 5731, 5741, 5751, 5760, 5771, 5781, 5791, 5800, 5811, 5821, 5831, 5841, 5850, 5861, 5871, 5881, 5890, 5901, 5911, 5921, 5930, 5941, 5951, 5961, 5971, 5981, 5991, 6001, 6011, 6020, 6031, 6041, 6051, 6060, 6071, 6081, 6091, 6100, 6111, 6121, 6131, 6141, 6151, 6161, 6171, 6181, 6190, 6201, 6211, 6221, 6230, 6241, 6251, 6261, 6270, 6281, 6291, 6301, 6311, 6320, 6331, 6341, 6351, 6360, 6371, 6381, 6391, 6400, 6411, 6421, 6431, 6440, 6451, 6461, 6471, 6481, 6490, 6501, 6511, 6521, 6530, 6541, 6551, 6561, 6570, 6581, 6591, 6601, 6611, 6621, 6631, 6641, 6651, 6660, 6671, 6681, 6691, 6700, 6711, 6721, 6731, 6740, 6751, 6761, 6771, 6781, 6791, 6801, 6811, 6821, 6830, 6841, 6851, 6861, 6870, 6881, 6891, 6901, 6910, 6921, 6931, 6941, 6951, 6960, 6971, 6981, 6991, 7000, 7011, 7021, 7031, 7040, 7051, 7061, 7071, 7080, 7091, 7101, 7111, 7121, 7130, 7141, 7151, 7161, 7170, 7181, 7191, 7201, 7210, 7221, 7231, 7241, 7251, 7261, 7271, 7281, 7291, 7300, 7311, 7321, 7331, 7340, 7351, 7361, 7371, 7380, 7391, 7401, 7411, 7421, 7431, 7441, 7451, 7461, 7470, 7481, 7491, 7501, 7510, 7521, 7531, 7541, 7550, 7561, 7571, 7581, 7591, 7600, 7611, 7621, 7631, 7640, 7651, 7661, 7671, 7680, 7691, 7701, 7711, 7720, 7731, 7741, 7751, 7761, 7770, 7781, 7791, 7801, 7810, 7821, 7831, 7841, 7850, 7861, 7871, 7881, 7891, 7901, 7911, 7921, 7931, 7940, 7951, 7961, 7971, 7980, 7991, 8001, 8011, 8020, 8031, 8041, 8051, 8061, 8071, 8081, 8091, 8101, 8110, 8121, 8131, 8141, 8150, 8161, 8171, 8181, 8190, 8201, 8211, 8221, 8231, 8240, 8251, 8261, 8271, 8280, 8291, 8301, 8311, 8320, 8331, 8341, 8351, 8360, 8371, 8381, 8391, 8401, 8410, 8421, 8431, 8441, 8450, 8461, 8471, 8481, 8490, 8501, 8511, 8521, 8531, 8541, 8551, 8561, 8571, 8580, 8591, 8601, 8611, 8620, 8631, 8641, 8651, 8660, 8671, 8681, 8691, 8701, 8711, 8721, 8731, 8741, 8750, 8761, 8771, 8781, 8790, 8801, 8811, 8821, 8830, 8841, 8851, 8861, 8871, 8880, 8891, 8901, 8911, 8920, 8931, 8941, 8951, 8960, 8971, 8981, 8991, 9000, 9011, 9021, 9031, 9041, 9050, 9061, 9071, 9081, 9090, 9101, 9111, 9121, 9130, 9141, 9151, 9161, 9171, 9181, 9191, 9201, 9211, 9220, 9231, 9241, 9251, 9260, 9271, 9281, 9291, 9300, 9311, 9321, 9331, 9341, 9351, 9361, 9371, 9381, 9390, 9401, 9411, 9421, 9430, 9441, 9451, 9461, 9470, 9481, 9491, 9501, 9511, 9520, 9531, 9541, 9551, 9560, 9571, 9581, 9591, 9600, 9611, 9621, 9631, 9640, 9651, 9661, 9671, 9681, 9690, 9701, 9711, 9721, 9730, 9741, 9751, 9761, 9770, 9781, 9791, 9801, 9811, 9821, 9831, 9841, 9851, 9860, 9871, 9881, 9891, 9900, 9911, 9921, 9931, 9940, 9951, 9961, 9971, 9981, 9991, 10001, 10011, 10021, 10030, 10041, ])
#no clutch the second group
velocity = np.array([-10, -20, -24, -32, -40, -44, -48, -52, -63, -71, -75, -80, -88, -93, -96, -101, -105, -112, -116, -120, -126, -128, -130, -134, -135, -139, -142, -141, -148, -147, -147, -147, -144, -144, -148, -147, -146, -145, -145, -140, -141, -139, -137, -135, -131, -128, -130, -126, -124, -121, -116, -111, -103, -103, -99, -95, -87, -82, -76, -70, -69, -62, -58, -50, -42, -38, -29, -25, -20, -13, -9, -1, 7, 10, 19, 24, 28, 37, 41, 43, 52, 57, 61, 67, 72, 74, 80, 82, 88, 95, 97, 97, 105, 106, 110, 112, 113, 118, 117, 119, 121, 124, 123, 126, 124, 126, 126, 126, 123, 123, 124, 122, 122, 117, 115, 115, 111, 114, 110, 109, 103, 99, 99, 93, 91, 86, 82, 81, 77, 73, 67, 62, 57, 51, 50, 41, 35, 34, 29, 25, 16, 11, 6, -1, -7, -11, -16, -21, -26, -32, -36, -44, -47, -52, -58, -59, -65, -71, -73, -76, -82, -84, -91, -93, -96, -101, -103, -104, -108, -111, -112, -114, -113, -116, -115, -113, -116, -118, -117, -117, -118, -118, -115, -116, -114, -115, -112, -110, -108, -105, -105, -103, -98, -99, -95, -91, -89, -83, -78, -77, -73, -66, -64, -61, -56, -54, -48, -46, -40, -31, -30, -24, -18, -13, -7, -6, 0, 4, 9, 11, 17, 23, 25, 30, 37, 40, 41, 48, 51, 53, 56, 63, 65, 69, 71, 75, 76, 78, 83, 84, 87, 88, 90, 93, 92, 94, 94, 95, 95, 98, 98, 97, 99, 94, 96, 97, 94, 91, 93, 90, 88, 87, 87, 85, 80, 81, 76, 74, 73, 69, 67, 62, 62, 56, 52, 49, 47, 44, 42, 35, 32, 31, 23, 21, 19, 13, 11, 5, -1, -2, -9, -12, -17, -20, -21, -28, -31, -33, -40, -44, -45, -49, -53, -55, -62, -60, -65, -69, -71, -72, -77, -76, -81, -80, -82, -84, -87, -86, -89, -88, -91, -91, -91, -91, -91, -88, -89, -89, -87, -84, -84, -82, -83, -81, -79, -76, -75, -73, -74, -68, -67, -65, -63, -61, -56, -56, -54, -49, -46, -44, -40, -35, -34, -30, -29, -25, -18, -16, -12, -9, -3, 0, 1, 5, 8, 10, 14, 18, 20, 24, 28, 30, 35, 33, 38, 42, 41, 46, 47, 49, 54, 56, 55, 56, 59, 61, 64, 63, 66, 65, 68, 67, 66, 66, 69, 69, 69, 69, 70, 66, 67, 67, 65, 62, 63, 60, 61, 58, 58, 57, 55, 53, 54, 52, 50, 48, 43, 44, 42, 37, 39, 33, 32, 30, 26, 23, 19, 18, 16, 11, 11, 9, 4, 3, -1, -5, -7, -8, -12, -14, -19, -21, -22, -26, -25, -30, -35, -33, -38, -39, -42, -43, -46, -47, -49, -52, -50, -52, -56, -58, -57, -60, -59, -58, -61, -61, -60, -60, -64, -60, -60, -61, -61, -61, -62, -59, -60, -56, -58, -55, -53, -54, -51, -49, -47, -48, -46, -44, -41, -42, -40, -38, -36, -33, -32, -27, -28, -26, -24, -22, -18, -19, -14, -13, -10, -6, -5, -2, -1, 1, 1, 7, 6, 11, 13, 11, 17, 16, 17, 19, 22, 24, 26, 25, 27, 29, 32, 31, 34, 33, 35, 35, 37, 37, 40, 39, 42, 42, 42, 42, 41, 41, 41, 41, 41, 41, 42, 42, 39, 40, 40, 37, 38, 39, 36, 33, 34, 31, 29, 29, 27, 28, 26, 27, 24, 22, 19, 20, 18, 19, 17, 11, 12, 10, 8, 9, 3, 5, 2, 1, -1, -3, -5, -4, -6, -8, -11, -13, -12, -14, -16, -15, -18, -20, -23, -22, -24, -23, -26, -25, -28, -31, -30, -29, -32, -31, -35, -34, -34, -33, -37, -36, -36, -36, -36, -36, -36, -36, -36, -36, -36, -33, -34, -34, -35, -31, -32, -29, -30, -31, -28, -25, -26, -23, -25, -22, -23, -20, -17, -19, -16, -13, -15, -12, -13, -10, -8, -9, -6, -4, -5, -2, 0, -1, 1, 0, 3, 2, 4, 4, 7, 6, 9, 8, 11, 10, 9, 13, 12, 11, 15, 14, 14, 17, 16, 16, 16, 15, 19, 18, 18, 18, 18, 18, 18, 17, 18, 18, 18, 18, 18, 18, 18, 19, 19, 15, 16, 17, 17, 14, 14, 15, 15, 12, 13, 13, 10, 11, 8, 9, 6, 6, 4, 4, 5, 2, 0, 0, -1, -1, -3, -3, -2, -5, -4, -7, -6, -5, -9, -11, -11, -10, -10, -12, -12, -11, -14, -14, -13, -17, -16, -16, -19, -19, -18, -18, -18, -21, -21, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -20, -21, -17, -17, -18, -18, -19, -15, -16, -16, -17, -14, -14, -15, -12, -12, -13, -10, -11, -8, -8, -9, -6, -7, -4, -4, -5, -2, -3, 0, -1, -1, 1, 0, 3, 2, 2, 2, 5, 4, 4, 7, 7, 6, 6, 6, 9, 8, 8, 8, 8, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 10, 11, 11, 11, 8, 8, 8, 9, 9, 5, 6, 6, 7, 4, 4, 5, 5, 2, 2, 3, 3, 0, 1, -1, -1, 0, -3, -3, -2, -2, -5, -4, -4, -4, -7, -7, -6, -5, -9, -8, -8, -11, -11, -10, -10, -10, -10, -13, -13, -13, -12, -12, -12, -11, -11, -11, -15, -15, -15, -11, -15, -15, -15, -15, -15, -15, -15, -11, -12, -12, -12, -12, ])
time = np.array([0, 10, 19, 30, 40, 50, 59, 70, 80, 90, 100, 109, 120, 130, 140, 149, 160, 170, 180, 189, 200, 210, 220, 229, 240, 250, 260, 270, 279, 290, 300, 310, 319, 330, 340, 350, 359, 370, 380, 390, 399, 410, 420, 430, 440, 449, 460, 470, 480, 489, 500, 510, 520, 529, 540, 550, 560, 570, 580, 590, 600, 610, 619, 630, 640, 650, 659, 670, 680, 690, 699, 710, 720, 730, 740, 749, 760, 770, 780, 789, 800, 810, 820, 829, 840, 850, 860, 869, 880, 890, 900, 910, 919, 930, 940, 950, 959, 970, 980, 990, 999, 1010, 1020, 1030, 1039, 1050, 1060, 1070, 1080, 1089, 1100, 1110, 1120, 1129, 1140, 1150, 1160, 1169, 1180, 1190, 1200, 1210, 1220, 1230, 1240, 1250, 1259, 1270, 1280, 1290, 1299, 1310, 1320, 1330, 1339, 1350, 1360, 1370, 1380, 1389, 1400, 1410, 1420, 1429, 1440, 1450, 1460, 1469, 1480, 1490, 1500, 1509, 1520, 1530, 1540, 1550, 1559, 1570, 1580, 1590, 1599, 1610, 1620, 1630, 1639, 1650, 1660, 1670, 1679, 1690, 1700, 1710, 1720, 1729, 1740, 1750, 1760, 1769, 1780, 1790, 1800, 1809, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1899, 1910, 1920, 1930, 1939, 1950, 1960, 1970, 1979, 1990, 2000, 2010, 2020, 2029, 2040, 2050, 2060, 2069, 2080, 2090, 2100, 2109, 2120, 2130, 2140, 2149, 2160, 2170, 2180, 2190, 2199, 2210, 2220, 2230, 2239, 2250, 2260, 2270, 2279, 2290, 2300, 2310, 2319, 2330, 2340, 2350, 2360, 2369, 2380, 2390, 2400, 2409, 2420, 2430, 2440, 2449, 2460, 2470, 2480, 2490, 2500, 2510, 2520, 2530, 2539, 2550, 2560, 2570, 2579, 2590, 2600, 2610, 2619, 2630, 2640, 2650, 2660, 2669, 2680, 2690, 2700, 2709, 2720, 2730, 2740, 2749, 2760, 2770, 2780, 2789, 2800, 2810, 2820, 2830, 2839, 2850, 2860, 2870, 2879, 2890, 2900, 2910, 2919, 2930, 2940, 2950, 2959, 2970, 2980, 2990, 3000, 3009, 3020, 3030, 3040, 3049, 3060, 3070, 3080, 3089, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3179, 3190, 3200, 3210, 3219, 3230, 3240, 3250, 3259, 3270, 3280, 3290, 3300, 3309, 3320, 3330, 3340, 3349, 3360, 3370, 3380, 3389, 3400, 3410, 3420, 3429, 3440, 3450, 3460, 3470, 3479, 3490, 3500, 3510, 3519, 3530, 3540, 3550, 3559, 3570, 3580, 3590, 3599, 3610, 3620, 3630, 3640, 3649, 3660, 3670, 3680, 3689, 3700, 3710, 3720, 3729, 3740, 3750, 3760, 3770, 3780, 3790, 3800, 3810, 3819, 3830, 3840, 3850, 3859, 3870, 3880, 3890, 3899, 3910, 3920, 3930, 3940, 3949, 3960, 3970, 3980, 3989, 4000, 4010, 4020, 4029, 4040, 4050, 4060, 4069, 4080, 4090, 4100, 4110, 4119, 4130, 4140, 4150, 4159, 4170, 4180, 4190, 4199, 4210, 4220, 4230, 4239, 4250, 4260, 4270, 4280, 4289, 4300, 4310, 4320, 4329, 4340, 4350, 4360, 4369, 4380, 4390, 4400, 4410, 4420, 4430, 4440, 4450, 4459, 4470, 4480, 4490, 4499, 4510, 4520, 4530, 4539, 4550, 4560, 4570, 4580, 4589, 4600, 4610, 4620, 4629, 4640, 4650, 4660, 4669, 4680, 4690, 4700, 4709, 4720, 4730, 4740, 4750, 4759, 4770, 4780, 4790, 4799, 4810, 4820, 4830, 4839, 4850, 4860, 4870, 4879, 4890, 4900, 4910, 4920, 4929, 4940, 4950, 4960, 4969, 4980, 4990, 5000, 5009, 5020, 5030, 5040, 5050, 5060, 5070, 5080, 5090, 5099, 5110, 5120, 5130, 5139, 5150, 5160, 5170, 5179, 5190, 5200, 5210, 5220, 5229, 5240, 5250, 5260, 5269, 5280, 5290, 5300, 5309, 5320, 5330, 5340, 5349, 5360, 5370, 5380, 5390, 5399, 5410, 5420, 5430, 5439, 5450, 5460, 5470, 5479, 5490, 5500, 5510, 5519, 5530, 5540, 5550, 5560, 5569, 5580, 5590, 5600, 5609, 5620, 5630, 5640, 5649, 5660, 5670, 5680, 5690, 5700, 5710, 5720, 5730, 5739, 5750, 5760, 5770, 5779, 5790, 5800, 5810, 5819, 5830, 5840, 5850, 5860, 5869, 5880, 5890, 5900, 5909, 5920, 5930, 5940, 5949, 5960, 5970, 5980, 5989, 6000, 6010, 6020, 6030, 6039, 6050, 6060, 6070, 6079, 6090, 6100, 6110, 6119, 6130, 6140, 6150, 6159, 6170, 6180, 6190, 6200, 6209, 6220, 6230, 6240, 6249, 6260, 6270, 6280, 6289, 6300, 6310, 6320, 6330, 6340, 6350, 6360, 6370, 6379, 6390, 6400, 6410, 6419, 6430, 6440, 6450, 6459, 6470, 6480, 6490, 6500, 6509, 6520, 6530, 6540, 6549, 6560, 6570, 6580, 6589, 6600, 6610, 6620, 6629, 6640, 6650, 6660, 6670, 6679, 6690, 6700, 6710, 6719, 6730, 6740, 6750, 6759, 6770, 6780, 6790, 6799, 6810, 6820, 6830, 6840, 6849, 6860, 6870, 6880, 6889, 6900, 6910, 6920, 6929, 6940, 6950, 6960, 6970, 6980, 6990, 7000, 7010, 7019, 7030, 7040, 7050, 7059, 7070, 7080, 7090, 7099, 7110, 7120, 7130, 7140, 7149, 7160, 7170, 7180, 7189, 7200, 7210, 7220, 7229, 7240, 7250, 7260, 7269, 7280, 7290, 7300, 7310, 7319, 7330, 7340, 7350, 7359, 7370, 7380, 7390, 7399, 7410, 7420, 7430, 7439, 7450, 7460, 7470, 7480, 7489, 7500, 7510, 7520, 7529, 7540, 7550, 7560, 7569, 7580, 7590, 7600, 7610, 7620, 7630, 7640, 7650, 7659, 7670, 7680, 7690, 7699, 7710, 7720, 7730, 7739, 7750, 7760, 7770, 7780, 7789, 7800, 7810, 7820, 7829, 7840, 7850, 7860, 7869, 7880, 7890, 7900, 7909, 7920, 7930, 7940, 7950, 7959, 7970, 7980, 7990, 7999, 8010, 8020, 8030, 8039, 8050, 8060, 8070, 8079, 8090, 8100, 8110, 8120, 8129, 8140, 8150, 8160, 8169, 8180, 8190, 8200, 8209, 8220, 8230, 8240, 8250, 8260, 8270, 8280, 8290, 8299, 8310, 8320, 8330, 8339, 8350, 8360, 8370, 8379, 8390, 8400, 8410, 8420, 8429, 8440, 8450, 8460, 8469, 8480, 8490, 8500, 8509, 8520, 8530, 8540, 8549, 8560, 8570, 8580, 8590, 8599, 8610, 8620, 8630, 8639, 8650, 8660, 8670, 8679, 8690, 8700, 8710, 8719, 8730, 8740, 8750, 8760, 8769, 8780, 8790, 8800, 8809, 8820, 8830, 8840, 8849, 8860, 8870, 8880, 8890, 8900, 8910, 8920, 8930, 8939, 8950, 8960, 8970, 8979, 8990, 9000, 9010, ])

velocity = np.array([-18, -16, -13, -8, -2, 1, 2, 73, -15, 33, 1, -20, -2, -20, 15, -27, -5, -26, 8, -2, 23, -1, 14, -14, -3, -17, -1, -14, -8, -17, -18, -7, 0, 3, -2, -3, -10, 0, 0, 7, -1, 1, -4, 0, -5, 0, -9, -8, -11, -15, -7, -13, -10, -14, -15, -13, -19, -18, -10, -2, -2, 0, 0, 1, 1, 0, -2, -7, -7, -4, -1, 0, 0, 0, -3, 0, 0, -2, -4, -4, -2, -1, 1, 0, -3, -5, -2, -2, -3, -2, -2, -3, -1, -1, 0, -2, -5, -2, -2, -3, -3, -3, -3, 0, 0, -2, -1, -9, -17, -19, -29, -31, -41, -48, -51, -57, -65, -71, -75, -78, -84, -91, -95, -98, -106, -106, -112, -117, -118, -122, -123, -125, -129, -129, -133, -132, -135, -138, -138, -138, -137, -137, -137, -133, -135, -133, -134, -131, -129, -125, -125, -122, -121, -117, -119, -116, -113, -108, -103, -100, -97, -92, -89, -84, -78, -72, -72, -66, -58, -53, -47, -42, -37, -32, -29, -20, -15, -11, -3, 11, 20, 13, 12, 11, 15, 18, 11, 7, -1, -1, -5, -3, -8, -8, -7, -2, -2, -1, -4, -5, -4, 0, -2, -3, 0, 0, 2, 2, 3, 1, 0, -2, -2, -7, -9, -6, -7, -5, -2, -3, -1, 1, 2, 3, 3, 0, 0, -5, -4, -7, -6, -4, -5, -3, 0, 0, -1, -1, 1, 0, -3, -2, -2, -2, -2, -5, -5, -2, -3, 0, 0, 0, 0, 0, 0, -3, -2, -2, -2, -3, -3, -3, -2, -3, -3, -3, -2, -3, -3, -3, 0, 0, -3, -3, -3, -2, -2, -2, -5, -6, 0, 0, 7, 18, 15, 30, 32, 35, 42, 43, 49, 55, 57, 63, 62, 71, 73, 74, 78, 84, 84, 91, 90, 91, 97, 98, 98, 101, 102, 102, 104, 104, 103, 106, 107, 108, 106, 103, 105, 102, 101, 100, 98, 98, 94, 97, 92, 90, 87, 87, 84, 82, 79, 76, 73, 68, 67, 63, 61, 58, 51, 49, 43, 40, 38, 32, 26, 25, 19, 13, 11, 5, 57, -6, -6, 12, -43, -1, -36, 1, -25, 0, -22, 0, -13, 5, 0, 12, 6, 7, -3, 1, -1, 5, -1, -4, -1, -10, -9, -9, -5, 0, -1, 1, 4, 3, 0, -2, -1, -3, 0, -7, -7, -6, -3, -3, 0, -3, -1, -3, 3, -1, -1, -5, -2, -5, -3, -2, -3, -5, -3, 0, -1, -3, -3, -2, 0, 0, 0, -2, -5, -2, -3, 0, -2, -2, -5, -2, 0, 0, -3, -3, 0, -3, 0, -2, -5, -5, -2, -2, -3, -3, -2, -3, 0, 0, -3, -2, -2, -2, -2, -2, -3, -7, -11, -11, -16, -27, -34, -26, -38, -35, -43, -50, -45, -57, -55, -60, -62, -64, -71, -70, -70, -78, -72, -83, -78, -83, -85, -84, -88, -84, -86, -88, -86, -88, -89, -87, -88, -86, -89, -87, -84, -85, -83, -80, -81, -79, -75, -72, -73, -72, -72, -66, -68, -66, -61, -62, -58, -53, -52, -47, -45, -41, -37, -39, -31, -27, -25, -22, -19, -13, -8, -8, -2, 15, 0, 4, 5, 17, 16, 11, 9, 5, 5, 0, -4, -9, -10, -8, -4, -2, -3, -2, 1, 0, -1, -7, -7, -8, -4, -4, 0, 0, 1, 3, 5, 2, 1, -3, -4, -6, -6, -8, -9, -7, -3, -1, 0, 0, 0, 1, -1, -3, -5, -7, -6, -4, -5, -3, 0, -1, 1, 1, -1, -2, -5, -4, -5, -5, -2, -3, 0, -1, 1, -1, -3, -2, -2, -2, -5, -5, -5, -2, 0, -1, 0, 0, 0, 0, -2, -2, -5, -5, -2, -3, -3, 0, 0, 0, 0, -3, -2, -4, -1, -2, 9, 8, 9, 16, 19, 22, 19, 26, 25, 28, 36, 33, 38, 41, 43, 46, 46, 50, 47, 54, 54, 53, 55, 55, 56, 60, 59, 62, 61, 61, 64, 64, 60, 64, 60, 64, 61, 60, 58, 59, 60, 56, 57, 55, 50, 51, 52, 49, 50, 48, 46, 46, 41, 41, 40, 38, 36, 34, 33, 30, 25, 23, 22, 21, 18, 17, 13, 10, 9, 7, 0, -13, -4, -10, 2, -7, -1, -12, -13, -14, -17, -18, -23, -14, -13, -7, -3, -1, 3, 4, 3, 4, 0, -3, -5, -5, -4, -5, -7, -4, -3, 3, 3, 3, 0, -3, -2, -2, -4, -4, -7, -2, -1, 0, 0, 0, 1, 1, 0, -3, -7, -6, -6, -4, -5, -3, -1, 1, 3, 2, 0, -3, -2, -4, -4, -6, -7, -6, -5, 0, 1, 0, 0, 1, -1, 0, -3, -7, -6, -5, -4, -5, 0, -3, -1, 1, 0, 1, -3, -2, -4, -4, -4, -4, -5, -2, 0, -1, 1, -4, -4, 0, -8, -8, -13, -19, -13, -22, -18, -23, -23, -20, -31, -28, -30, -29, -34, -36, -35, -36, -39, -40, -42, -42, -42, -43, -43, -45, -45, -45, -47, -45, -48, -47, -48, -47, -48, -47, -48, -46, -45, -43, -46, -43, -41, -41, -42, -40, -37, -38, -35, -36, -36, -33, -34, -31, -30, -31, -27, -26, -26, -24, -22, -23, -21, -18, -16, -14, -12, -10, -8, -9, 21, 12, -7, -1, -4, 2, 8, 6, 6, 9, 8, 7, 4, -1, -4, -6, -7, -4, -5, -7, 0, 0, 0, 1, 0, -4, -4, -7, -7, -6, -6, -7, -2, -1, -1, 1, 0, 0, 0, 0, -3, -4, -7, -3, -5, -5, -2, -3, -1, 1, 1, -1, -3, -2, -5, -4, -4, -4, -4, -2, -1, -1, 1, -1, -1, 0, -2, -5, -4, -4, -5, -2, -2, -3, 0, -1, 1, -1, 0, -2, -2, -5, -5, -5, -5, -3, 0, -1, -1, -1, 0, 0, -3, -2, -5, -5, -5, -2, -3, -3, 1, 0, -1, 3, 3, 7, 4, 9, 6, 13, 7, 13, 13, 13, 17, 14, 19, 16, 19, 18, 17, 20, 20, 19, 19, 21, 23, 25, 22, 21, 21, 24, 24, 24, 24, 21, 24, 25, 25, 22, 22, 22, 22, 22, 19, 20, 21, 17, 18, 19, 16, 17, 13, 14, 15, 12, 13, 10, 11, 8, 9, 7, 7, 2, -11, -5, -3, -10, -2, 1, -3, -8, -11, -11, -12, -16, -10, -9, -9, -10, -13, -12, -9, -7, -2, -5, 0, 1, 2, 3, 0, 0, -1, -1, 0, 0, -3, -3, -5, -2, -2, -2, -4, -5, -5, -2, -5, -4, -4, -2, -3, -1, -1, 0, -1, 0, -1, 0, -3, -2, -3, -2, -3, -5, -5, -4, -1, -5, -2, -5, -3, 0, ])
time = np.array([0, 10, 20, 29, 40, 50, 60, 69, 80, 90, 100, 110, 120, 130, 140, 150, 159, 170, 180, 190, 199, 210, 220, 230, 239, 250, 260, 270, 280, 289, 300, 310, 320, 329, 340, 350, 360, 369, 380, 390, 400, 409, 420, 430, 440, 450, 459, 470, 480, 490, 499, 510, 520, 530, 539, 550, 560, 570, 579, 590, 600, 610, 620, 629, 640, 650, 660, 669, 680, 690, 700, 709, 720, 730, 740, 750, 760, 770, 780, 790, 799, 810, 820, 830, 839, 850, 860, 870, 879, 890, 900, 910, 920, 929, 940, 950, 960, 969, 980, 990, 1000, 1009, 1020, 1030, 1040, 1049, 1060, 1070, 1080, 1090, 1099, 1110, 1120, 1130, 1139, 1150, 1160, 1170, 1179, 1190, 1200, 1210, 1219, 1230, 1240, 1250, 1260, 1269, 1280, 1290, 1300, 1309, 1320, 1330, 1340, 1349, 1360, 1370, 1380, 1390, 1400, 1410, 1420, 1430, 1439, 1450, 1460, 1470, 1479, 1490, 1500, 1510, 1519, 1530, 1540, 1550, 1560, 1569, 1580, 1590, 1600, 1609, 1620, 1630, 1640, 1649, 1660, 1670, 1680, 1689, 1700, 1710, 1720, 1730, 1739, 1750, 1760, 1770, 1779, 1790, 1800, 1810, 1819, 1830, 1840, 1850, 1859, 1870, 1880, 1890, 1900, 1909, 1920, 1930, 1940, 1949, 1960, 1970, 1980, 1989, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2079, 2090, 2100, 2110, 2119, 2130, 2140, 2150, 2159, 2170, 2180, 2190, 2200, 2209, 2220, 2230, 2240, 2249, 2260, 2270, 2280, 2289, 2300, 2310, 2320, 2329, 2340, 2350, 2360, 2370, 2379, 2390, 2400, 2410, 2419, 2430, 2440, 2450, 2459, 2470, 2480, 2490, 2499, 2510, 2520, 2530, 2540, 2549, 2560, 2570, 2580, 2589, 2600, 2610, 2620, 2629, 2640, 2650, 2660, 2670, 2680, 2690, 2700, 2710, 2719, 2730, 2740, 2750, 2759, 2770, 2780, 2790, 2799, 2810, 2820, 2830, 2840, 2849, 2860, 2870, 2880, 2889, 2900, 2910, 2920, 2929, 2940, 2950, 2960, 2969, 2980, 2990, 3000, 3010, 3019, 3030, 3040, 3050, 3059, 3070, 3080, 3090, 3099, 3110, 3120, 3130, 3139, 3150, 3160, 3170, 3180, 3189, 3200, 3210, 3220, 3229, 3240, 3250, 3260, 3269, 3280, 3290, 3300, 3310, 3320, 3330, 3340, 3350, 3359, 3370, 3380, 3390, 3399, 3410, 3420, 3430, 3439, 3450, 3460, 3470, 3480, 3489, 3500, 3510, 3520, 3529, 3540, 3550, 3560, 3569, 3580, 3590, 3600, 3609, 3620, 3630, 3640, 3650, 3659, 3670, 3680, 3690, 3699, 3710, 3720, 3730, 3739, 3750, 3760, 3770, 3779, 3790, 3800, 3810, 3820, 3829, 3840, 3850, 3860, 3869, 3880, 3890, 3900, 3909, 3920, 3930, 3940, 3950, 3960, 3970, 3980, 3990, 3999, 4010, 4020, 4030, 4039, 4050, 4060, 4070, 4079, 4090, 4100, 4110, 4120, 4129, 4140, 4150, 4160, 4169, 4180, 4190, 4200, 4209, 4220, 4230, 4240, 4249, 4260, 4270, 4280, 4290, 4299, 4310, 4320, 4330, 4339, 4350, 4360, 4370, 4379, 4390, 4400, 4410, 4419, 4430, 4440, 4450, 4460, 4469, 4480, 4490, 4500, 4509, 4520, 4530, 4540, 4549, 4560, 4570, 4580, 4590, 4600, 4610, 4620, 4630, 4639, 4650, 4660, 4670, 4679, 4690, 4700, 4710, 4719, 4730, 4740, 4750, 4760, 4769, 4780, 4790, 4800, 4809, 4820, 4830, 4840, 4849, 4860, 4870, 4880, 4889, 4900, 4910, 4920, 4930, 4939, 4950, 4960, 4970, 4979, 4990, 5000, 5010, 5019, 5030, 5040, 5050, 5059, 5070, 5080, 5090, 5100, 5109, 5120, 5130, 5140, 5149, 5160, 5170, 5180, 5189, 5200, 5210, 5220, 5230, 5240, 5250, 5260, 5270, 5279, 5290, 5300, 5310, 5319, 5330, 5340, 5350, 5359, 5370, 5380, 5390, 5400, 5409, 5420, 5430, 5440, 5449, 5460, 5470, 5480, 5489, 5500, 5510, 5520, 5529, 5540, 5550, 5560, 5570, 5579, 5590, 5600, 5610, 5619, 5630, 5640, 5650, 5659, 5670, 5680, 5690, 5699, 5710, 5720, 5730, 5740, 5749, 5760, 5770, 5780, 5789, 5800, 5810, 5820, 5829, 5840, 5850, 5860, 5870, 5880, 5890, 5900, 5910, 5919, 5930, 5940, 5950, 5959, 5970, 5980, 5990, 5999, 6010, 6020, 6030, 6040, 6049, 6060, 6070, 6080, 6089, 6100, 6110, 6120, 6129, 6140, 6150, 6160, 6169, 6180, 6190, 6200, 6210, 6219, 6230, 6240, 6250, 6259, 6270, 6280, 6290, 6299, 6310, 6320, 6330, 6339, 6350, 6360, 6370, 6380, 6389, 6400, 6410, 6420, 6429, 6440, 6450, 6460, 6469, 6480, 6490, 6500, 6510, 6520, 6530, 6540, 6550, 6559, 6570, 6580, 6590, 6599, 6610, 6620, 6630, 6639, 6650, 6660, 6670, 6680, 6689, 6700, 6710, 6720, 6729, 6740, 6750, 6760, 6769, 6780, 6790, 6800, 6809, 6820, 6830, 6840, 6850, 6859, 6870, 6880, 6890, 6899, 6910, 6920, 6930, 6939, 6950, 6960, 6970, 6979, 6990, 7000, 7010, 7020, 7029, 7040, 7050, 7060, 7069, 7080, 7090, 7100, 7109, 7120, 7130, 7140, 7150, 7160, 7170, 7180, 7190, 7199, 7210, 7220, 7230, 7239, 7250, 7260, 7270, 7279, 7290, 7300, 7310, 7320, 7329, 7340, 7350, 7360, 7369, 7380, 7390, 7400, 7409, 7420, 7430, 7440, 7449, 7460, 7470, 7480, 7490, 7499, 7510, 7520, 7530, 7539, 7550, 7560, 7570, 7579, 7590, 7600, 7610, 7619, 7630, 7640, 7650, 7660, 7669, 7680, 7690, 7700, 7709, 7720, 7730, 7740, 7749, 7760, 7770, 7780, 7790, 7800, 7810, 7820, 7830, 7839, 7850, 7860, 7870, 7879, 7890, 7900, 7910, 7919, 7930, 7940, 7950, 7960, 7969, 7980, 7990, 8000, 8009, 8020, 8030, 8040, 8049, 8060, 8070, 8080, 8089, 8100, 8110, 8120, 8130, 8139, 8150, 8160, 8170, 8179, 8190, 8200, 8210, 8219, 8230, 8240, 8250, 8259, 8270, 8280, 8290, 8300, 8309, 8320, 8330, 8340, 8349, 8360, 8370, 8380, 8389, 8400, 8410, 8420, 8430, 8440, 8450, 8460, 8470, 8479, 8490, 8500, 8510, 8519, 8530, 8540, 8550, 8559, 8570, 8580, 8590, 8600, 8609, 8620, 8630, 8640, 8649, 8660, 8670, 8680, 8689, 8700, 8710, 8720, 8729, 8740, 8750, 8760, 8770, 8779, 8790, 8800, 8810, 8819, 8830, 8840, 8850, 8859, 8870, 8880, 8890, 8899, 8910, 8920, 8930, 8940, 8949, 8960, 8970, 8980, 8989, 9000, 9010, 9020, 9029, 9040, 9050, 9060, 9070, 9080, 9090, 9100, 9110, 9119, 9130, 9140, 9150, 9159, 9170, 9180, 9190, 9199, 9210, 9220, 9230, 9240, 9249, 9260, 9270, 9280, 9289, 9300, 9310, 9320, 9329, 9340, 9350, 9360, 9369, 9380, 9390, 9400, 9410, 9419, 9430, 9440, 9450, 9459, 9470, 9480, 9490, 9499, 9510, 9520, 9530, 9539, 9550, 9560, 9570, 9580, 9589, 9600, 9610, 9620, 9629, 9640, 9650, 9660, 9669, 9680, 9690, 9700, 9710, 9720, 9730, 9740, 9750, 9759, 9770, 9780, 9790, 9799, 9810, 9820, 9830, 9839, 9850, 9860, 9870, 9880, 9889, 9900, 9910, 9920, 9929, 9940, 9950, 9960, 9969, 9980, 9990, 10000, 10009, 10020, 10030, 10040, 10050, 10059, 10070, 10080, 10090, 10099, 10110, 10120, 10130, 10139, 10150, 10160, 10170, 10179, 10190, 10200, 10210, 10220, 10229, 10240, 10250, 10260, 10269, 10280, 10290, 10300, 10309, 10320, 10330, 10340, 10350, 10360, 10370, 10380, 10390, 10399, 10410, 10420, 10430, 10439, 10450, 10460, 10470, 10479, 10490, 10500, 10510, 10520, 10529, 10540, 10550, 10560, 10569, 10580, 10590, 10600, 10609, 10620, 10630, 10640, 10649, 10660, 10670, 10680, 10690, 10699, 10710, 10720, 10730, 10739, 10750, 10760, 10770, 10779, 10790, 10800, 10810, 10819, 10830, 10840, 10850, 10860, 10869, 10880, 10890, 10900, 10909, 10920, 10930, 10940, 10949, 10960, 10970, 10980, 10990, ])


fig, ax1 = plt.subplots(figsize=(6.5, 4), dpi=100)
ax2 = ax1.twinx()

# ax1.plot(time, angle, 'k-*', label='Degree')
ax1.plot(time, velocity,'r-*', label='Speed')
# ax2.plot(time, stage,'b-*', label='Clutching Stage')

# ax1.set_ylabel('Degree [°]',fontweight ='bold')
ax1.set_ylabel('Speed [°/s]',fontweight ='bold')
# ax2.set_ylabel('Stage',fontweight ='bold')

ax1.set_xlabel('Time [ms]', fontweight ='bold')

ax1.grid()
# ax1.set_ylim([-40, 40])
ax1.set_ylim([-200, 200])
# ax2.set_ylim([-2, 2])
fig.legend()
fig.savefig('sample.pdf')
plt.show()


