using System;

namespace frontend.model
{
    class StockPrice
    {
        public string Code { get; set; }

        public Decimal Open { get; set; }

        public Decimal High { get; set; }

        public Decimal Low { get; set; }

        public Decimal Close { get; set; }

        public DateTime Date { get; set; }

        public int Vol { get; set; }

        public bool Enable { get; set; }
    }
}
