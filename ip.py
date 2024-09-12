from typing import Union

class IP:
    def __init__(self):
        self.member = [128, 64, 32, 16, 8, 4, 2, 1]

    @staticmethod
    def decToBin(dec: Union[str, int]) -> str:
        dec = int(dec)
        return f"{bin(dec)[2:]:0>8}"

    @staticmethod
    def binToDec(_bin: str) -> str:
        return str(int(_bin, 2))

    """
    revBin
    from: 00001111
    to:   11110000
    """
    @staticmethod
    def revBin(_bin: str) -> str:
        temp = ""
        for char in _bin:
            if char == '0':
                temp = temp + '1'
            else:
                temp = temp + '0'
        return temp

    """
    把1.1.1.1/21中的21提取出来, 并且转换为
    """
    @staticmethod
    def fill(digit: Union[str, int]) -> str:
        digit = int(digit)
        return '1' * digit + '0' * (32 - digit)

    # 找到网段的开头
    def findStart(self, num: Union[str, int], maskNum: Union[str, int]) -> str:
        """
        计算网段开头
        rule: 网络/位数
        from: 123.155.158.1/5
        to:   120.0.0.0
        01111011因为前五个都为1所以前5位不变, 后面使用0补充
        01111000 = 120

        :param num: 传入当前需要计算网段的段
        :param maskNum: 子网掩码位数
        :return:
        """
        num = int(num)
        _bin = self.decToBin(num)
        return self.binToDec(f"{_bin[0: int(maskNum) % 8]:0<8}")

    # 找到网段的结尾
    def findEnd(self, startNum: Union[str, int], maskNum: Union[str, int]) -> str:
        maskNum = int(maskNum)
        _maskNum = maskNum % 8
        _tmp = "1" * _maskNum + "0" * (8 - _maskNum)
        _bin = self.revBin(_tmp)
        _dec = self.binToDec(_bin)
        return str(int(startNum) + int(_dec))

    @staticmethod
    def isIp(ip: str) -> bool:
        fragment = ip.split(".")
        for i in fragment:
            if 0 <= int(i) <= 255:
                pass
            else:
                return False
        return True

    def isLan(self, _lan: str) -> bool:
        pass

    def lan(self, _lan: str) -> list:
        """
        计算区间
        123.155.158.1/11
        ['123.128.0.0', '123.159.255.255']

        :param _lan: 网段 (123.155.158.1/11)
        :return:
        """
        ip, maskNum = _lan.split("/")
        if self.isIp(ip):
            fragment = ip.split(".")
            maskNum = int(maskNum)
            same = int(maskNum / 8) # 不变的段
            if same < 4:
                temp = ""
                for i in range(same):
                    temp = temp + fragment[i] + "."
                start = self.findStart(fragment[same], maskNum)
                end = self.findEnd(start, maskNum)
                start = temp + start + "." + "0." * (4 - (same + 1))
                end = temp + end + "." + "255." * (4 - (same + 1))
                return [start[: len(start) - 1], end[: len(end) - 1]]
            else:
                return [ip, ip]
        else:
            return ['-1.-1.-1.-1', '-1.-1.-1.-1']

    def inLan(self, _ip: str, _lan: str) -> bool:
        if self.isIp(_ip):
            startLan, endLan = self.lan(_lan)
            startLanFragment = startLan.split(".")
            endLanFragment = endLan.split(".")
            checkIpFragment = _ip.split(".")
            for i in range(4):
                if int(startLanFragment[i]) <= int(checkIpFragment[i]) <= int(endLanFragment[i]):
                    pass
                else:
                    return False
            return True
        else:
            return False

if __name__ == '__main__':
    ip = IP()
    # print(ip.decToBin(188))                         # 10000000
    # print(ip.binToDec(ip.decToBin(128)))            # 128
    # print(ip.revBin(ip.decToBin(128)))              # 01111111
    # print(ip.binToDec(ip.revBin(ip.decToBin(128)))) # 127
    # print(ip.fill(21))
    # print(ip.lan("123.155.158.1/10"))

    # 计算区间
    # print(ip.lan("131.0.72.0/25"))

    # 判断ip是否在区间中
    print(ip.inLan("116.193.88.1", "116.193.89.0/21"))
