using System;
using System.Collections.Generic;
using System.Data.Linq;
using System.Data.SQLite;

namespace frontend.db
{
    public class DBManager
    {
        private const string ConnectionString = @" DataSource = ..\..\..\..\backend\main_db.sqlite3";

        public T Query<T>(Func<DataContext, T> query)
        {
            using (var cn = new SQLiteConnection(ConnectionString))
            {
                cn.Open();
                using (var cmd = new SQLiteCommand(cn))
                {
                    using (var context = new DataContext(cn))
                    {
                        return query(context);
                    }
                }
            }
        }

        public IReadOnlyList<T> QueryList<T>(Func<DataContext, List<T>> query)
        {
            var resultList = new List<T>();

            using (var cn = new SQLiteConnection(ConnectionString))
            {
                cn.Open();
                using (var cmd = new SQLiteCommand(cn))
                {
                    using (var context = new DataContext(cn))
                    {
                        resultList = query(context);
                        //var table = context.GetTable<BackendResult>();

                        ////foreach (var q in table.Where(x => x.id == "01GVY3BXMEQJ2GJ9MF6WYATEMW").OrderByDescending(x => x.seq))
                        //foreach (var b in table.OrderByDescending(x => x.Seq))
                        //{
                        //    resultList.Add(new BackendResult() { Id = b.Id, Result = b.Result, Created = b.Created, Modified = b.Modified });
                        //}
                    }
                }
                return resultList;
            }
        }

        public T Mutate<T>(Func<DataContext, T> mutate)
        {
            using (var cn = new SQLiteConnection(ConnectionString))
            {
                cn.Open();
                using (var cmd = new SQLiteCommand(cn))
                {
                    using (var context = new DataContext(cn))
                    {
                        return mutate(context);
                    }
                }
            }
        }
    }
}
