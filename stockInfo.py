import requests
from globalVar import log


class StockInfo(object):
    """股票信息对象"""
    dictStock = {}  # 存放股票代码及查询链接
    stockData = []  # 存放获取到的股票信息

    def __init__(self, se, monitoredStock):
        """构造函数，初始化要监控的股票极其链接.
        Args:
            se:交易所消息（交易所:链接），列表类型
            monitoredStock:要监控的股票代码，字典类型，键为交易所名，值为股票代码列表
        """
        self.monitoredStock = monitoredStock
        self.s = requests.session()
        self.s.keep_alive = False

        dict_se = {}
        for el in se:
            dict_se.update({el.split(': ')[0]: el.split(': ')[1]})
        for key in monitoredStock:
            for stockid in monitoredStock[key]:
                StockInfo.dictStock.update({stockid: dict_se[key] + stockid})

    def __get_data(self, url):
        """获取股票数据.

        Args:
            url:股票的链接
        """
        try:
            response = self.s.get(url)
            response.raise_for_status()
            response.close()
        except Exception as info:
            log.logger.error(info)
        else:
            jsonData = response.json()
            StockInfo.stockData.append((jsonData["snap"][0], jsonData["code"], jsonData["snap"][5], jsonData["snap"][7], jsonData["snap"]
                                        [6], jsonData["snap"][1], jsonData["snap"][2], jsonData["snap"][3], jsonData["snap"][4], jsonData["time"]))
            log.logger.info("{}({}) 现价：{:<7.2f} 涨幅：{:<7.2f} 涨跌：{:<6.2f} 昨收：{:<7.2f} 开盘：{:<7.2f} 最高：{:<7.2f} 最低：{:<7.2f} 交易时间：{}".format(
                jsonData["snap"][0], jsonData["code"], jsonData["snap"][5], jsonData["snap"][7], jsonData["snap"][6], jsonData["snap"][1], jsonData["snap"][2], jsonData["snap"][3], jsonData["snap"][4], jsonData["time"]))

    def get_all_stock_info(self):
        """获取所有的股票信息."""
        StockInfo.stockData.clear()
        for url in StockInfo.dictStock.values():
            StockInfo.__get_data(self, url)
        log.logger.info("")
        StockInfo.stockData.sort(
            key=lambda stock: stock[3], reverse=True)  # 以涨幅进行排序

    def display_stock_info(self):
        """显示所有的股票信息"""
        for data in StockInfo.stockData:
            print("{}({}) 现价：{:<7.2f} 涨幅：{:7s} 涨跌：{:<6.2f} 昨收：{:<7.2f} 开盘：{:<7.2f} 最高：{:<7.2f} 最低：{:<7.2f} 交易时间：{}".format(
                data[0], data[1], data[2], str(data[3])+"%", data[4], data[5], data[6], data[7], data[8], data[9]), sep="")
