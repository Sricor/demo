# coding:utf-8
# 作者：Sricor
# 日期：2021.2.13
# 天气推送
import re
import requests

class Weather():
    def __init__(self, lat, lng): #经纬度
        self.lat = lat
        self.lng = lng

    def getData(self):
        url = 'https://weather.com/zh-CN/weather/today/l/%s,%s' % (self.lat, self.lng)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

        data = requests.get(url=url, headers=headers).text

        city = re.findall(r'<h1 class="CurrentConditions--location--1Ayv3">(.*?)</h1>', data)[0] # 城市
        deadline = re.findall(r'<div class="CurrentConditions--timestamp--1SWy5">(.*?)</div>', data)[0] # 截止时间
        temperature = re.findall(r'<div class="CurrentConditions--tempHiLoValue--A4RQE"><span data-testid="TemperatureValue">(.*?)</span>/<span data-testid="TemperatureValue">(.*?)</span></div>', data)[0] # 最高低温度
        feel_temperature = re.findall(r'<span data-testid="TemperatureValue" class="CurrentConditions--tempValue--3KcTQ">(.*?)</span>', data)[0] # 体感温度
        type = re.findall(r'<div data-testid="wxPhrase" class="CurrentConditions--phraseValue--2xXSr">(.*?)</div>', data)[0] #天气类型

        humidity = re.findall(r'<span data-testid="PercentageValue">(.*?)</span>', data)[0] # 湿度
        pressure = re.findall(r'<div data-testid="wxData" class="WeatherDetailsListItem--wxData--23DP5"><span data-testid="PressureValue" class="Pressure--pressureWrapper--3olKd undefined">(.*?)</span>', data)[0] # 气压
        yisibility = re.findall(r'<div data-testid="wxData" class="WeatherDetailsListItem--wxData--23DP5"><span data-testid="VisibilityValue">(.*?)</span>', data)[0] # 能见度
        wind = re.findall(r'<path stroke="currentColor" fill="none" d="M18.467 4.482l-5.738 5.738a1.005 1.005 0 0 1-1.417 0L5.575 4.482l6.446 16.44 6.446-16.44z"></path></svg>(.*?)</span>', data)[0] # 风
        dew = re.findall(r'<div data-testid="wxData" class="WeatherDetailsListItem--wxData--23DP5"><span data-testid="TemperatureValue">(.*?)</span>', data)[1] # 露点
        uv = re.findall(r'<div data-testid="wxData" class="WeatherDetailsListItem--wxData--23DP5"><span data-testid="UVIndexValue">(.*?)</span>', data)[0] # 紫外线指数
        moon = re.findall(r'<div data-testid="WeatherDetailsLabel" class="WeatherDetailsListItem--label--3JSSI">月相</div><div data-testid="wxData" class="WeatherDetailsListItem--wxData--23DP5">(.*?)</div>', data)[0] # 月相

        air = re.findall(r'<span class="AirQualityText--severity--1VMr2" data-testid="AirQualityCategory">(.*?)</span><p class="AirQualityText--severityText--3QoOU" data-testid="AirQualitySeverity">(.*?)</p>', data)[0] # 空气质量指数
        health = re.findall(r'<h3 data-testid="ListTitle" class="HealthActivitiesListItem--heading--3D3xX">(.*?)</h3><p data-testid="Description" class="HealthActivitiesListItem--description--1Ilem">(.*?)</p>', data)[0] # 健康与活动


        data_temperature = re.findall(r'<div data-testid="SegmentHighTemp" class="Column--temp--2v_go"><span data-testid="TemperatureValue">(.*?)</span></div>', data)[0:4] # 温度数据
        data_rain = re.findall(r'<span class="Column--precip--2H5Iw"><span class="Accessibility--visuallyHidden--1432w">降雨几率</span>(.*?)</span>',data)[0:4]  # 降雨数据

        high_temperature = temperature[0] # 最高温
        low_temperature = temperature[1] # 最低温

        t_early = data_temperature[0] # 上午温度
        t_midday = data_temperature[1] # 中午温度
        t_afternoon = data_temperature[2] # 晚上温度
        t_midnight = data_temperature[3] # 夜间温度

        r_early = data_rain[0] # 上午降雨
        r_midday = data_rain[1] # 中午降雨
        r_afternoon = data_rain[2] # 晚上降雨
        r_midnight = data_rain[3] # 夜间降雨

        early = '上午%s，有%s的降雨概率' % (t_early, r_early)
        midday = '下午%s，有%s的降雨概率' % (t_midday, r_midday)
        afternoon = '晚上%s，有%s的降雨概率' % (t_afternoon, r_afternoon)
        midnight = '夜间%s，有%s的降雨概率' % (t_midnight, r_midnight)
        temperature = '高/低：%s/%s' % (high_temperature, low_temperature)

        info = '***天气推送***<br/>' \
               '%s。<br/>天气：%s。<br/>温度：%s。<br/>%s。<br/>' \
               '%s。<br/>%s。<br/>%s。<br/>%s。<br/>' \
               '%s。<br/>湿度：%s。<br/>能见度：%s。<br/>' \
               '风速：%s。<br/>露点：%s。<br/>紫外线：%s。<br/>月相：%s。<br/>' \
               '空气质量：%s；%s<br/>' \
               '健康活动：%s。<br/>' \
               '每天都要开心，祝您生活愉快！ <br/>' % (city, type, feel_temperature, deadline, early, midday, afternoon, midnight, temperature,humidity, yisibility, wind, dew, uv, moon, air[0], air[1], health[1])

        return info

if __name__ == '__main__':
    result = Weather(25.78, 113.10).getData()

    with open('weather.html', 'w') as c:
        c.write(result)

