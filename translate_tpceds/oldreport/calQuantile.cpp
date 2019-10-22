double CDSDriver::CalQuantile(vector<double> vTime, QUANTILE quan)
{
        if (vTime.size() < 1)   // 返回容器中实际数据的个数。
        {
                return -1;
        }
        std::sort(vTime.begin(), vTime.end()); // vTime.begin()传回迭代器中的第一个数据地址; VTime.end()指向迭代器中末端元素的下一个
        double dQuantile = -1;
        double dQ = 0;
        int iIndex = 0;
        switch (quan)
        {
        case CDSDriver::Q1:
                dQ = (double)(vTime.size() + 1) / 4;
                iIndex = floor(dQ);
                if ((dQ - iIndex) == 0)
                {
                        dQuantile = vTime.at(iIndex - 1);
                }
                else
                {
                        dQuantile = vTime.at(iIndex - 1) * 0.25 + vTime.at(iIndex) * 0.75;
                }
                break;
        case CDSDriver::Q2:
                dQ = (double)2 * (vTime.size() + 1) / 4;
                iIndex = floor(dQ);
                if ((dQ - iIndex) == 0)
                {
                        dQuantile = vTime.at(iIndex - 1);
                }
                else
                {
                        dQuantile = vTime.at(iIndex - 1) * 0.5 + vTime.at(iIndex) * 0.5;
                }
                break;
        case CDSDriver::Q3:
                dQ = (double)3 * (vTime.size() + 1) / 4;
                iIndex = floor(dQ);
                if ((dQ - iIndex) == 0)
                {
                        dQuantile = vTime.at(iIndex - 1);
                }
                else
                {
                        dQuantile = vTime.at(iIndex - 1) * 0.75 + vTime.at(iIndex) * 0.25;
                }
                break;
        default:
                break;
        }
        return dQuantile;
}
