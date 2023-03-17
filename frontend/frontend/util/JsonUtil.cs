using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Unicode;

namespace frontend.util
{
    public class JsonUtil
    {
        private static JsonSerializerOptions defaultJsonSerializerOptions = new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.Create(UnicodeRanges.All),
            //WriteIndented = true
        };

        public static string ToJson(object obj)
        {
            var jsonStr = JsonSerializer.Serialize(obj, defaultJsonSerializerOptions);
            return jsonStr;
        }
    }
}
