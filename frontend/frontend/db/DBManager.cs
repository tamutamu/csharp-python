using frontend.model;
using System.Collections.Generic;
using System.Data.Linq;
using System.Data.SQLite;
using System.Linq;

namespace frontend.db
{
    public class DBManager
    {
        public List<BackendResult> QueryList()
        {
            List<BackendResult> resultList = new List<BackendResult>();

            using (var cn = new SQLiteConnection(@" DataSource = ..\..\..\..\backend\main_db.sqlite3"))
            {
                cn.Open();
                using (var cmd = new SQLiteCommand(cn))
                {
                    using (var context = new DataContext(cn))
                    {
                        var table = context.GetTable<BackendResult>();

                        //foreach (var q in table.Where(x => x.id == "01GVY3BXMEQJ2GJ9MF6WYATEMW").OrderByDescending(x => x.seq))
                        foreach (var b in table.OrderByDescending(x => x.Seq))
                        {
                            resultList.Add(new BackendResult() { Id = b.Id, Result = b.Result, Created = b.Created, Modified = b.Modified });
                        }
                    }
                }
                return resultList;
            }
        }
    }
}
