using System;
using System.Data.Linq.Mapping;
using System.Text.Json.Serialization;

namespace frontend.model
{
    [Table(Name = "backend_result")]
    public class BackendResult
    {
        [Column(Name = "id", CanBeNull = false, DbType = "NVARCHAR", IsPrimaryKey = true)]
        public string Id { get; set; }

        [Column(Name = "seq", CanBeNull = false, DbType = "INT", IsPrimaryKey = true)]
        public int Seq { get; set; }

        [Column(Name = "result", CanBeNull = true, DbType = "NVARCHAR")]
        public string Result { get; set; }

        [Column(Name = "created", CanBeNull = false, DbType = "DATETIME")]
        public DateTime Created { get; set; }

        [Column(Name = "modified", CanBeNull = false, DbType = "DATETIME")]
        public DateTime Modified { get; set; }
    }

    public class StockPrice
    {
        [JsonPropertyName("code")]
        public string Code { get; set; }

        [JsonPropertyName("open")]
        public Decimal Open { get; set; }

        [JsonPropertyName("high")]
        public Decimal High { get; set; }

        [JsonPropertyName("low")]
        public Decimal Low { get; set; }

        [JsonPropertyName("close")]
        public Decimal Close { get; set; }

        [JsonPropertyName("date")]
        public DateTime Date { get; set; }

        [JsonPropertyName("vol")]
        public int Vol { get; set; }

        [JsonPropertyName("enable")]
        public bool Enable { get; set; }
    }
}
