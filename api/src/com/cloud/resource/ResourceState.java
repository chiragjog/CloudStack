package com.cloud.resource;

import java.util.List;
import java.util.Set;

import com.cloud.utils.fsm.StateMachine;

public enum ResourceState {
    Enabled,
    Disabled,
    Unmanaged,
    PrepareForMaintenance,
    ErrorInMaintenance,
    Maintenance;
    
    public enum Event {
        InternalCreated("Resource is created"),
        Enable("Admin enables"),
        Disable("Admin disables"),
        AdminAskMaintenace("Admin asks to enter maintenance"),
        AdminCancelMaintenance("Admin asks to cancel maintenance"),
        InternalEnterMaintenance("Resource enters maintenance"),
        Unmanaged("Admin turns a host into umanaged state"),
        UpdatePassword("Admin updates password of host"),
        UnableToMigrate("Management server migrates VM failed"),
        DeleteHost("Admin delete a host");
        
        private final String comment;
        private Event(String comment) {
            this.comment = comment;
        }
        
        public String getDescription() {
            return this.comment;
        }
    }
    
    public ResourceState getNextState(Event a) {
        return s_fsm.getNextState(this, a);
    }
    
    public ResourceState[] getFromStates(Event a) {
        List<ResourceState> from = s_fsm.getFromStates(this, a);
        return from.toArray(new ResourceState[from.size()]);
    }
    
    public Set<Event> getPossibleEvents() {
        return s_fsm.getPossibleEvents(this);
    }
    
    public static String[] toString(ResourceState... states) {
        String[] strs = new String[states.length];
        for (int i=0; i<states.length; i++) {
            strs[i] = states[i].toString();
        }
        return strs;
    }
    
    protected static final StateMachine<ResourceState, Event> s_fsm = new StateMachine<ResourceState, Event>();
    static {
        s_fsm.addTransition(null, Event.InternalCreated, ResourceState.Enabled);
        s_fsm.addTransition(ResourceState.Enabled, Event.Enable, ResourceState.Enabled);
        s_fsm.addTransition(ResourceState.Enabled, Event.Disable, ResourceState.Disabled);
        s_fsm.addTransition(ResourceState.Enabled, Event.Unmanaged, ResourceState.Unmanaged);
        s_fsm.addTransition(ResourceState.Enabled, Event.AdminAskMaintenace, ResourceState.PrepareForMaintenance);
        s_fsm.addTransition(ResourceState.Disabled, Event.Enable, ResourceState.Enabled);
        s_fsm.addTransition(ResourceState.Disabled, Event.Disable, ResourceState.Disabled);
        s_fsm.addTransition(ResourceState.Disabled, Event.Unmanaged, ResourceState.Unmanaged);
        s_fsm.addTransition(ResourceState.Unmanaged, Event.Unmanaged, ResourceState.Unmanaged);
        s_fsm.addTransition(ResourceState.PrepareForMaintenance, Event.InternalEnterMaintenance, ResourceState.Maintenance);
        s_fsm.addTransition(ResourceState.PrepareForMaintenance, Event.AdminCancelMaintenance, ResourceState.Enabled);
        s_fsm.addTransition(ResourceState.PrepareForMaintenance, Event.Unmanaged, ResourceState.Unmanaged);
        s_fsm.addTransition(ResourceState.Maintenance, Event.AdminCancelMaintenance, ResourceState.Enabled);
        s_fsm.addTransition(ResourceState.Maintenance, Event.DeleteHost, ResourceState.Disabled);
        s_fsm.addTransition(ResourceState.Maintenance, Event.Unmanaged, ResourceState.Unmanaged);
        s_fsm.addTransition(ResourceState.ErrorInMaintenance, Event.Unmanaged, ResourceState.Unmanaged);
        s_fsm.addTransition(ResourceState.ErrorInMaintenance, Event.Disable, ResourceState.Disabled);
        s_fsm.addTransition(ResourceState.ErrorInMaintenance, Event.DeleteHost, ResourceState.Disabled);
        s_fsm.addTransition(ResourceState.ErrorInMaintenance, Event.InternalEnterMaintenance, ResourceState.Maintenance);
    }
}