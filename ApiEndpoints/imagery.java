import java.util.HashMap;

public static class imagery{

    public imagery(String IP, int PORT){
        String server_ip = IP;
        int server_port = PORT; 
        String[] addresses = {};
        String[] areas = {};

        // self.area_payload = {
        //     "service_type":"image_collection",
        //     "service_name":"redfin",
        //     "client_request_data":{
        //         "filters":[""],
        //         "listing_requested":{
        //             "type":"city&state",
        //             "area":[],
        //             "storage":"cache"
        //             }
        //     }
        // }
        
        HashMap<String, String> area_payload = new HashMap<>();


        HashMap<String, String> client_request_data = new HashMap<>();
        HashMap<String, String> listing_requested = new HashMap<>();

        
        client_request_data.put("filters", String[""]);
        client_request_data.put("listing_requested", listing_requested);
        
        area_payload.put("service_type", "image_collection");
        area_payload.put("service_name", "redfin");
        area_payload.put("client_request_data", client_request_data);
    }

    public String get_images_with_areas(String[] areas){

    }

    public String get_images_with_addresses(String[] addresses){

    }

}