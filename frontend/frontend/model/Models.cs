using System;
using System.Collections.Generic;
using System.Data.Linq;
using System.Data.Linq.Mapping;
using System.Linq;
using System.Text.Json.Serialization;

namespace frontend.model
{
    [Table(Name = "setting")]
    public class Setting
    {
        [Column(Name = "name", CanBeNull = false, DbType = "NVARCHAR", IsPrimaryKey = true)]
        public string Name { get; set; }

        [Column(Name = "value", CanBeNull = false, DbType = "NVARCHAR")]
        public string Value { get; set; }

        [Column(Name = "created", CanBeNull = false, DbType = "DATETIME")]
        public DateTime Created { get; set; }

        [Column(Name = "modified", CanBeNull = false, DbType = "DATETIME")]
        public DateTime Modified { get; set; }

        static public Func<DataContext, Setting> GetQuery(string name)
        {
            Func<DataContext, Setting> _query = (context) =>
            {
                var entity = context.GetTable<Setting>().Where(e => e.Name == name).SingleOrDefault();
                return entity;
            };
            return _query;
        }

        static public Func<DataContext, List<Setting>> createEntity = (context) =>
        {
            var list = new List<Setting>();
            foreach (var b in context.GetTable<Setting>())
            {
                list.Add(new Setting() { Name = b.Name, Value = b.Value, Created = b.Created, Modified = b.Modified });
            }
            return list;
        };

        public Func<DataContext, Setting> GetMutate()
        {
            Func<DataContext, Setting> _mutate = (context) =>
            {
                var entity = context.GetTable<Setting>().Where(e => e.Name == this.Name).SingleOrDefault();
                if (entity != null)
                {
                    entity.Value = this.Value;
                }
                else
                {
                    var s = new Setting() { Name = this.Name, Value = this.Value };
                    context.GetTable<Setting>().InsertOnSubmit(s);
                }
                context.SubmitChanges();
                return entity;
            };
            return _mutate;
        }
    }

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

        static public Func<DataContext, List<BackendResult>> createEntity = (context) =>
        {
            var list = new List<BackendResult>();
            foreach (var b in context.GetTable<BackendResult>().OrderByDescending(x => x.Seq))
            {
                list.Add(new BackendResult() { Id = b.Id, Result = b.Result, Created = b.Created, Modified = b.Modified });
            }
            return list;
        };
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
