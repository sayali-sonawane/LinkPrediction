# from matplotlib import pyplot
#
# dict1 = {0: 0, 1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 3, 8: 3, 9: 3, 10: 3, 11: 4, 12: 4, 13: 4, 14: 4, 15: 5, 16: 5, 17: 5, 18: 5, 19: 6, 20: 6, 21: 6, 22: 7, 23: 7, 24: 7, 25: 7, 26: 7, 27: 7, 28: 8, 29: 9, 30: 9, 31: 9, 32: 9, 33: 10, 34: 10, 35: 10, 36: 12, 37: 12, 38: 12, 39: 12, 40: 12, 41: 12, 42: 14, 43: 14, 44: 15, 45: 15, 46: 15, 47: 16, 48: 16, 49: 16, 50: 16, 51: 17, 52: 18, 53: 18, 54: 18, 55: 18, 56: 18, 57: 19, 58: 19, 59: 20, 60: 20, 61: 20, 62: 21, 63: 22, 64: 22, 65: 23, 66: 24, 67: 24, 68: 24, 69: 24, 70: 24, 71: 25, 72: 25, 73: 27, 74: 27, 75: 27, 76: 28, 77: 28, 78: 29, 79: 29, 80: 29, 81: 29, 82: 29, 83: 29, 84: 30, 85: 30, 86: 30, 87: 30, 88: 30, 89: 30, 90: 30, 91: 32, 92: 32, 93: 33, 94: 33, 95: 33, 96: 33, 97: 34, 98: 34, 99: 35}
# dict2 = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 16, 17: 16, 18: 17, 19: 18, 20: 19, 21: 20, 22: 21, 23: 22, 24: 23, 25: 24, 26: 25, 27: 26, 28: 27, 29: 28, 30: 29, 31: 30, 32: 31, 33: 32, 34: 33, 35: 34, 36: 35, 37: 36, 38: 36, 39: 37, 40: 37, 41: 37, 42: 38, 43: 39, 44: 40, 45: 41, 46: 42, 47: 43, 48: 44, 49: 45, 50: 46, 51: 47, 52: 48, 53: 49, 54: 50, 55: 51, 56: 52, 57: 53, 58: 54, 59: 55, 60: 56, 61: 57, 62: 58, 63: 58, 64: 59, 65: 60, 66: 60, 67: 60, 68: 61, 69: 62, 70: 63, 71: 64, 72: 65, 73: 66, 74: 67, 75: 68, 76: 69, 77: 70, 78: 71, 79: 72, 80: 73, 81: 74, 82: 75, 83: 76, 84: 77, 85: 78, 86: 79, 87: 80, 88: 81, 89: 82, 90: 83, 91: 84, 92: 85, 93: 86, 94: 87, 95: 88, 96: 88, 97: 89, 98: 90, 99: 91}
#
# x = []
# y1 = []
# y2 = []
#
# for key, value in dict1.items():
#     x.append(key)
#     y1.append(value)
# for key, value in dict2.items():
#     y2.append(value)
#
# pyplot.plot(x,y1,label='Against greedy player')
# pyplot.plot(x,y2,label='Against random player')
# pyplot.xlabel('Games played')
# pyplot.ylabel('Games won')
# pyplot.legend()
# pyplot.show()

def swap(a):
    t = a[0]
    a[0] = a[1]
    a[1] = t

a = [1,2]
print(swap(a))